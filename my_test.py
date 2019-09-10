#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Nafisa Tabassum <nafisatabassum@3d-p.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: parse_interfaces

short_description: Parse an interfaces file

version_added: "2.8"

description:
    - "This test module will simply"

options:
    path:
        description:
            - The interfaces file to parse.
        type: path
        required: true
        aliases: [ filename ]

extends_documentation_fragment:
    - files

author:
    - Nafisa Tabassum (nafisatabassum@3d-p.com)
'''

EXAMPLES = '''
# Parse interfaces file
- name: Parse interfaces file and return a JSON file
  parse_interfaces:
    path: interfaces
'''

RETURN = '''
json:
    description: The JSON file that contains parsed key/value pairs the module generates
    type: file
    returned: always
'''

import debinterface
import json
import os 
import sys
from collections import OrderedDict
from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(type='path', required=True, aliases=['filename']),
            ),
            supports_check_mode=True,
        )

    path = module.params['path']
    network_interface_directory = "/etc/network/"
    if os.path.isfile(os.path.join(network_interface_directory, path)):
        network_interface_filepath = os.path.realpath(os.path.join(network_interface_directory, path))
    else:
        module.fail_json(msg="File %s was not found" % (path))

    network_interface_details = OrderedDict()
    exported_network_adapters = []
    interface_name = []
    interface_info = []
    interfaces_in_file = debinterface.Interfaces(interfaces_path=network_interface_filepath)
    adapters = interfaces_in_file.adapters

    for adapter in adapters:
        item = adapter.export()
        exported_network_adapters.append(item)
        interface_name.append(adapter.attributes["name"])

    for index, interface in enumerate(exported_network_adapters):
        interface_info.append(
            {
                "addrFam": interface.get("addrFam", None),
                "auto": interface.get("auto", None),
                "ip setting": interface.get("source", None),
                "address": interface.get("address", None),
                "netmask": interface.get("netmask", None),
                "gateway": interface.get("gateway", None),
                "up": interface.get("up", None),
                "down": interface.get("down", None),
                "pre-up": interface.get("pre-up", None),
                "pre-down": interface.get("pre-down", None),
                "post-up": interface.get("post-up", None),
                "post-down": interface.get("post-down", None),
                "bridge-opts": interface.get("bridge-opts", None),
                "wlan-opts": interface.get("unknown", None),
            }
        )

    for key, value in zip(interface_name, interface_info):
        network_interface_details.setdefault(key, []).append(value)

    with open("parsed_network_interfaces.json", "w") as json_file:
        json.dump(
            network_interface_details, json_file, indent=4, separators=(",", ": ")
        )

    module.exit_json(json=json_file)

if __name__ == '__main__':
    main()