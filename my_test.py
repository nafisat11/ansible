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
json_file:
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

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        path=dict(type='path', required=True, aliases=['filename'])
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()