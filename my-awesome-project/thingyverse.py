#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Evtech Solutions, Ltd.

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community',
}

DOCUMENTATION = """
    inventory: thingyverse
    version_added: "2.7"
    short_description: Enumerates everything defined in Thingyverse
    description:
      - Queries a given Thingyverse server and enumerates all found Things.
    extends_documentation_fragment:
      - constructed
    notes:
      - input must be a valid URL to the base-path of a Thingyverse server.
"""

import json
import urllib.parse
import urllib.request

from ansible.utils.display import Display
from ansible.plugins.inventory import BaseInventoryPlugin

_display = Display()


_TRAIT_PROCESSORS = {}

def _process_iep(inventory, thing_id):
    inventory.set_variable(thing_id, 'ansible_connection', 'ssh')
    inventory.set_variable(thing_id, 'ansible_ssh_user', 'root')
    inventory.set_variable(thing_id, 'ansible_ssh_pass', 'dponice')
_TRAIT_PROCESSORS['3d-p/insight/v1/device/3d-p/iep'] = _process_iep
del _process_iep


def _get_thingyverse_settings(config):
    if config.endswith('thingyverse.json'):
        try:
            config = json.loads(open(config, 'r').read())
            url = config['url']
            
            if urllib.parse.urlparse(url).netloc: #it's plausibly a URL
                return url
        except Exception as e:
            display.warning("unable to parse thingyverse config: {}".format(e))
    else:
        display.debug("thingyverse inventory filename must end with 'thingyverse.json'")
    return None
    
def _query_thingyverse(url):
    request = urllib.request.Request(
        url=url + '/thing',
        data=json.dumps({
            'jsonrpc': '2.0',
            'id': 0,
            'method': 'selectThings',
            'params': {
            },
        }).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
        },
    )
    things = urllib.request.urlopen(request).read()
    return json.loads(things)['result']
    
class InventoryModule(BaseInventoryPlugin):
    NAME='thingyverse'
    
    def verify_file(self, config):
        #config is a path supplied using '-i' on the commandline
        #It's expected to define how to access Thingyverse.
        if super(InventoryModule, self).verify_file(config):
            if _get_thingyverse_settings(config): #it's plausibly valid
                return True #signal that this module may be able to handle it
        return False
        
    def parse(self, inventory, loader, config, cache=False):
        super(InventoryModule, self).parse(inventory, loader, config)
        
        for (thing_id, thing) in _query_thingyverse(_get_thingyverse_settings(config)).items():
            traits = thing['traits']
            props = thing['props']
            tags = thing['tags']
            
            self.inventory.add_host(thing_id)
            host = self.inventory.get_host(thing_id)
            
            self.inventory.set_variable(thing_id, 'ansible_ssh_extra_args', '-o StrictHostKeyChecking=no')
            
            self.inventory.set_variable(thing_id, 'name', thing['name'])
            self.inventory.set_variable(thing_id, 'thing_id', thing_id)
            self.inventory.set_variable(thing_id, 'traits', traits)
            self.inventory.set_variable(thing_id, 'props', props)
            self.inventory.set_variable(thing_id, 'tags', tags)
            
            for tag in tags:
                tag = '%{}'.format(tag)
                
                try: #assume it's been seen before
                    group = self.inventory.groups[tag]
                except KeyError: #add it if needed
                    self.inventory.add_group(tag)
                    group = self.inventory.groups[tag]
                    
                group.add_host(host)
                
            for trait in traits:
                processor = _TRAIT_PROCESSORS.get(trait)
                if processor:
                    processor(self.inventory, thing_id)
                    
                trait_set = []
                fragment = '@'
                for trait_part in trait.split('/'):
                    fragment += trait_part
                    trait_set.append(fragment)
                    fragment += '/'
                    
                for (i, trait_part) in enumerate(trait_set):
                    try: #assume it's been seen before
                        group = self.inventory.groups[trait_part]
                    except KeyError: #add it if needed
                        self.inventory.add_group(trait_part)
                        group = self.inventory.groups[trait_part]
                        
                        if i > 0: #this trait is a child
                            parent_group = self.inventory.groups[trait_set[i - 1]]
                            if trait_part not in parent_group.child_groups:
                                parent_group.add_child_group(group)
                                
                    group.add_host(host)
                    
            #Extract location, if defined
            location = thing.get('location')
            if location:
                self.inventory.set_variable(thing_id, 'location', location['location']['coordinates'])
                
            ip_set = False
            #extract IP addresses, if defined
            if "3d-p/insight/v1/device/addresses" in thing['traits']:
                ipv4_addresses = props['v1-addresses'].get('ip4')
                if ipv4_addresses:
                    self.inventory.set_variable(thing_id, 'ipv4_addresses', ipv4_addresses)
                    if not ip_set:
                        self.inventory.set_variable(thing_id, 'ansible_host', ipv4_addresses[0])
                        ip_set = True
                ipv6_addresses = props['v1-addresses'].get('ip6')
                if ipv6_addresses:
                    self.inventory.set_variable(thing_id, 'ipv6_addresses', ipv6_addresses)
                    if not ip_set:
                        self.inventory.set_variable(thing_id, 'ansible_host', ipv6_addresses[0])
                        ip_set = True
                        
