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

short_description: Retreive model attributes

version_added: "2.8"

description:
    - This module will retrieve attributes like "wifi80211Count" from a model.

options:
    model:
        description:
            - Specific model
        type: str
        required: true

extends_documentation_fragment:
    - system

author:
    - Nafisa Tabassum (nafisatabassum@3d-p.com)
"""

EXAMPLES = """
# Add attributes to model
- model_spec:
    model: model
"""

RETURN = """
model_attribs:
  description: JSON structure containing attributes for specified model
  returned: success
  type: dict
  sample: {
           'wifi80211Count': 1, 
           'lteCount': 0, 
           'rajantCount': 0, 
           'meaCount': 0, 
           'eth8023Count': 4, 
           'serial232Count': 6, 
           'canCount': 0, 
           'c2020Count': 0, 
           'c5915Count': 0, 
           'family': 'e55', 
           'platform': 'r3'
        }
"""
import json
from ansible.module_utils.basic import AnsibleModule

MODELS = """{
    "hor-e55-80211": {
        "wifi80211Count": 1,
        "lteCount": 0,
        "rajantCount": 0,
        "meaCount": 0,
        "eth8023Count": 4,
        "serial232Count": 6,
        "canCount": 0,
        "c2020Count": 0,
        "c5915Count": 0,
        "family": "e55",
        "platform": "r3"
    },
    "hor-e55-solo": {
        "wifi80211Count": 0,
        "lteCount": 0,
        "rajantCount": 0,
        "meaCount": 1,
        "eth8023Count": 4,
        "serial232Count": 6,
        "canCount": 0,
        "c2020Count": 0,
        "c5915Count": 0,
        "family": "e55",
        "platform": "r3"
    },
    "hor-e56-80211": {
        "wifi80211Count": 1,
        "lteCount": 0,
        "rajantCount": 0,
        "meaCount": 0,
        "eth8023Count": 2,
        "serial232Count": 10,
        "canCount": 2,
        "c2020Count": 0,
        "c5915Count": 0,
        "family": "e56",
        "platform": "r3"
    },
    "hor-e56-solo": {
        "wifi80211Count": 0,
        "lteCount": 0,
        "rajantCount": 0,
        "meaCount": 1,
        "eth8023Count": 2,
        "serial232Count": 10,
        "canCount": 2,
        "c2020Count": 0,
        "c5915Count": 0,
        "family": "e56",
        "platform": "r3"
    },
    "hor-e57-nn": {
        "wifi80211Count": 2,
        "lteCount": 0,
        "rajantCount": 0,
        "meaCount": 0,
        "eth8023Count": 4,
        "serial232Count": 6,
        "canCount": 0,
        "c2020Count": 0,
        "c5915Count": 0,
        "family": "e57",
        "platform": "r3"
    },
    "hor-e57-n+cell-na": {
        "wifi80211Count": 1,
        "lteCount": 1,
        "rajantCount": 0,
        "meaCount": 0,
        "eth8023Count": 4,
        "serial232Count": 6,
        "canCount": 2,
        "c2020Count": 0,
        "c5915Count": 0,
        "family": "e57",
        "platform": "r3"
    },
    "hor-e57-n+cell-aus": {
        "wifi80211Count": 1,
        "lteCount": 1,
        "rajantCount": 0,
        "meaCount": 0,
        "eth8023Count": 4,
        "serial232Count": 6,
        "canCount": 2,
        "c2020Count": 0,
        "c5915Count": 0,
        "family": "e57",
        "platform": "r3"
    },
    "hor-e57-n+solo": {
        "wifi80211Count": 1,
        "lteCount": 0,
        "rajantCount": 0,
        "meaCount": 1,
        "eth8023Count": 4,
        "serial232Count": 6,
        "canCount": 2,
        "c2020Count": 0,
        "c5915Count": 0,
        "family": "e57",
        "platform": "r3"
    },
    "hor-e58-n": {
        "wifi80211Count": 1,
        "lteCount": 0,
        "rajantCount": 0,
        "meaCount": 0,
        "eth8023Count": 2,
        "serial232Count": 6,
        "canCount": 0,
        "c2020Count": 0,
        "c5915Count": 0,
        "family": "e58",
        "platform": "r3"
    },
    "hor-e58-solo": {
        "wifi80211Count": 0,
        "lteCount": 0,
        "rajantCount": 0,
        "meaCount": 1,
        "eth8023Count": 2,
        "serial232Count": 6,
        "canCount": 0,
        "c2020Count": 0,
        "c5915Count": 0,
        "family": "e58",
        "platform": "r3"
    },
    "phm-e15": {
        "wifi80211Count": 0,
        "lteCount": 0,
        "rajantCount": 0,
        "meaCount": 0,
        "eth8023Count": 2,
        "serial232Count": 2,
        "canCount": 0,
        "c2020Count": 0,
        "c5915Count": 0,
        "family": "e15",
        "platform": "r3"
    },
    "sab-1s1e80211": {
        "wifi80211Count": 1,
        "lteCount": 0,
        "rajantCount": 0,
        "meaCount": 0,
        "eth8023Count": 1,
        "serial232Count": 1,
        "canCount": 0,
        "c2020Count": 0,
        "c5915Count": 0,
        "family": "e30",
        "platform": "r3"
    },
    "sab-1s1esolo": {
        "wifi80211Count": 0,
        "lteCount": 0,
        "rajantCount": 0,
        "meaCount": 1,
        "eth8023Count": 1,
        "serial232Count": 1,
        "canCount": 0,
        "c2020Count": 0,
        "c5915Count": 0,
        "family": "e30",
        "platform": "r3"
    }
}"""


def main():
    module = AnsibleModule(
        argument_spec=dict(model=dict(type="str", required=True)),
        supports_check_mode=True,
    )
    model = module.params["model"]
    attribs = json.loads(MODELS)
    model_attribs = None
    exception = ""

    try:
        model_attribs = attribs[model]
    except KeyError as err:
        exception = err

    module.exit_json(changed=True, model_attribs=model_attribs, exception=exception)


if __name__ == "__main__":
    main()
