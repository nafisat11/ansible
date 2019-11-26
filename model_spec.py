#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Nafisa Tabassum <nafisatabassum@3d-p.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
module: model_spec

short_description: Add attributes to model

version_added: "2.8"

description:
    - This module will add attributes like "has_wifi" to a model.

options:
    model:
        description:
            - Specific model
        type: str
        required: true
    attrib:
        description:
            - Model-specific attributes you want to add
        type: list
        elements: str
        required: true

extends_documentation_fragment:
    - system

author:
    - Nafisa Tabassum (nafisatabassum@3d-p.com)
"""

EXAMPLES = """
# Add attributes to model
- model_spec:
    model: "{ model }"
    attrib: ["needs_crda"]
"""

RETURN = """
"""

from ansible.module_utils.basic import AnsibleModule

model_attribs = {}

def main():
    module = AnsibleModule(
        argument_spec=dict(
            model=dict(type="str", required=True),
            attrib=dict(type="list", required=True),
        ),
        supports_check_mode=True,
    )
    model = module.params["model"]
    attrib = module.params["attrib"]

    model_attribs[model] = attrib

    module.exit_json(changed=True, model_attribs=model_attribs)

if __name__ == "__main__":
    main()