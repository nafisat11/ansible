import json
import argparse
import os
import sys
from collections import OrderedDict
from pprint import pprint as pp
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        "-f",
        type=str,
        help="Enter the name of the network interface file you wish to parse",
        action="store",
    )
    args = parser.parse_args()

    filename = args.file
    network_interface_directory = "/home/nafisa/Documents/"
    if os.path.isfile(os.path.join(network_interface_directory, filename)):
        network_interface_filepath = os.path.realpath(
            os.path.join(network_interface_directory, filename)
        )
    else:
        print("Please enter valid network interfaces filename")
        sys.exit(1)

    header = {"version":"0.0.0"}
    interfaces_json_model = {}
    network_interface_details = OrderedDict()

    with open(network_interface_filepath) as interfaces_file:
        is_interface_stanza = False
        stanza = []
        keywords = ("auto", "iface", "post-up", "post-down")
        for line in interfaces_file:
            line = line.strip().split("#")[0]

            #line = re.sub("^(\s*\r?\n){2,}", "\r\n", line)
            line = re.sub("[ \t]*\n{3,}", "\n\n", line)

            if line.startswith(keywords):
                interfaces = {}
                if not interfaces:
                    stanza.append(interfaces)
                is_interface_stanza = True

            elif not line:
                is_interface_stanza = False

            if is_interface_stanza:
                interfaces[line.split()[0]] = line.split()[1:]

                
    interfaces_json_model["header"] = header
    interfaces_json_model["interfaces_data"] = network_interface_details


    with open("parsed_network_interfaces.json", "w") as json_file:
        json.dump(
            interfaces_json_model, json_file, indent=4, separators=(",", ": ")
        )


if __name__ == "__main__":
    main()
