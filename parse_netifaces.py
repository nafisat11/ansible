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
        interfaces = {}
        non_auto_ifaces = []
        auto_ifaces = []
        inet_ifaces = []
        inet6_ifaces = []
        for line in interfaces_file:
            line = line.strip().split("#")[0]

            #line = re.sub("^(\s*\r?\n){2,}", "\r\n", line)
            if not line.strip():
                continue

            line = line.split()
            if "iface" in line:
                if "inet" in line:
                    inet_ifaces.append(line[1])
                if "inet6" in line:
                    inet6_ifaces.append(line[1])

                if line[1] in interfaces:
                    continue
                interfaces[line[1]] = {}
                for iface in inet_ifaces:
                    if iface in interfaces:
                        interfaces[iface] = {"inet":{}}
                for iface in inet6_ifaces:
                    if iface in interfaces and "inet" in interfaces[iface]:
                        interfaces[iface] = {"inet":{}, "inet6": {}}
        

            if "auto" in line:
                auto_ifaces.append(line[1])

                #if line[1] in interfaces:
                    #continue
                #interfaces[line[1]] = {}
            for iface_auto_true in auto_ifaces:
                if iface_auto_true in inet_ifaces:
                    interfaces[iface_auto_true]["inet"].update({"auto":"true"})

            print(auto_ifaces)



        pp(interfaces["eth0"])

        









            #if line.startswith("auto"):
                #interfaces = {}
                #if not interfaces:
                    #stanza.append(interfaces)
                #is_interface_stanza = True
                #pass



            #if is_interface_stanza:
                #if line == "":
                    #continue
                #interfaces[line.split()[0]] = line.split()[1:]





                #if line.startswith("auto")
                    #stanza.append(line)
                #if line.startswith("auto"):
                    #stanza.append(line)



    interfaces_json_model["header"] = header
    interfaces_json_model["interfaces_data"] = interfaces


    with open("parsed_network_interfaces.json", "w") as json_file:
        json.dump(
            interfaces_json_model, json_file, indent=4, separators=(",", ": ")
        )


if __name__ == "__main__":
    main()
