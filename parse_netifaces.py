import json
import argparse
import os
import sys
from collections import OrderedDict


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
    interfaces = {}

    with open(network_interface_filepath) as interfaces_file:
        is_interface_stanza = False
        interfaces = []
        for line in interfaces_file:
            """if line.strip().startswith("#"):
                continue
            line = line.split("#")[0]
            if not line.strip():
                continue"""
            line = line.strip().split("#")[0]
            if not line.strip() or line.startswith("source"):
                continue
            #print(line)

            if line.startswith("auto"):
                auto_line = line.split()
                interfaces = {}
                if not interfaces:
                    
                interfaces = {auto_line[1]:[]}
                print(interfaces)           

                #print(auto_line)
        
            #inet6_ifaces = []
            #if line.startswith("iface"):
                #iface_line = line.split()
                #iface = iface_line[1]
                #mode = iface_line[3]
                #if "inet" in iface_line:
                    #network_interface_details[iface] = {"inet":{"mode":mode}}

                #elif "inet6" in iface_line:
                    #network_interface_details[iface].update({"inet6":{"mode":mode}})"""





    
    interfaces_json_model["header"] = header
    interfaces_json_model["interfaces_data"] = network_interface_details


    with open("parsed_network_interfaces.json", "w") as json_file:
        json.dump(
            interfaces_json_model, json_file, indent=4, separators=(",", ": ")
        )


if __name__ == "__main__":
    main()
