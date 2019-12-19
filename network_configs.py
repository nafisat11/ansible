import json
import argparse
import os

from iface_configs import *
from rajant_configs import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file", "-f", type=str, help="Enter the name of the json file", action="store"
    )
    args = parser.parse_args()

    filename = args.file
    json_directory = "/home/nafisa/ansible-playbooks/"
    if os.path.isfile(os.path.join(json_directory, filename)):
        json_filepath = os.path.realpath(os.path.join(json_directory, filename))
    else:
        print("Please enter valid filename")
        sys.exit(1)

    with open(json_filepath) as json_file:
        data_structure = json.load(json_file)
        interfaces_data = data_structure["data"]["interfaces"]
        rajant_data = data_structure["data"]["rajant"]
        for iface in interfaces_data.keys():
            auto_prop(interfaces_data, iface).add_line()
            addrFam(interfaces_data, iface).add_line()

        for breadcrumb in rajant_data["breadcrumbs"]:
            RajantConfig(breadcrumb).get_setting()
