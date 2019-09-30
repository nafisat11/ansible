import re
import argparse
import os
import sys
import json
import itertools
from collections import OrderedDict
from pprint import pprint as pp

def file_iterator():
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
    stanza = []

    with open(network_interface_filepath) as interfaces_file:
        for line in interfaces_file:
            line = line.split("#")[0]
            if line.isspace():
                if stanza:
                    yield "".join(stanza)
                    stanza = []
            else:
                stanza.append(line)
        if stanza:
            yield "".join(stanza)

def gen():
    lst = []
    network_stanza = file_iterator()
    for stanza in network_stanza:
        if not stanza:
            continue
        lst.append(stanza)
    fsm = Iface_Parse_FSM(lst)
    fsm.run()

    """auto = list(filter(lambda x: "auto" in x, line))
    inet = list(filter(lambda x: "inet" in x, line))
    vlan_opts = list(filter(lambda x: "vlan-" in x, line))
    network_interface_details[auto[0].split()[1]] = {"auto":"true", "addrFam":{"inet":{"mode":inet[0].split()[3]}}}
    network_interface_details["vlan10"]["addrFam"]["inet"] = {vlan_opts[0].strip().split()[0]:[]}
    if len(vlan_opts) > 1:
        for opt in vlan_opts:
            opt = opt.strip().split()[1]
            network_interface_details["vlan10"]["addrFam"]["inet"]["vlan-raw-device"].append(opt)

        #network_interface_details["vlan10"]["addrFam"]["inet"]["vlan-raw-device"]
    line2 = lst[4].split("\n")
    auto = list(filter(lambda x: "auto" in x, line2))
    vlan_opts = list(filter(lambda x: "vlan-" in x, line2))
    network_interface_details[auto[0].split()[1]] = {"auto":"true", "addrFam":{"inet":{vlan_opts[0].strip().split()[0]:[]}}}
    if len(vlan_opts) > 1:
        for opt in vlan_opts:
            opt = opt.strip().split()[1]
            network_interface_details[auto[0].split()[1]]["addrFam"]["inet"]["vlan-raw-device"].append(opt)"""
    
    

class Iface_Parse_FSM:
    interfaces_json_model = {}
    wlan_opts = {}
    bridge_opts = {}
    vlan_opts = {}
    mea_opts = OrderedDict()

    def __init__(self, data):
        self.data = data
        self.current_state = None
        self.next_state = None
        self.prev_state = None
        self.iter = 1
        self.prev_iface = None
        self.current_iface = None
        self.max_iter = None
        self.inet_iface = None
        self.inet6_iface = None
        self.network_interface_details = OrderedDict()

    def run(self):
        self.max_iter = len(self.data)
        self.next_state = self.interate_through_stanzas(self.iter)
        #self.iterate_through_lines(self.iter)

    def interate_through_stanzas(self, next_stanza):
        self.next_stanza = next_stanza
        self.next_state = self.process_stanza(self.data[self.next_stanza])

    def process_stanza(self, stanza):
        stanza = stanza.split("\n")
        auto = list(filter(lambda x: "auto" in x, stanza))
        self.next_state = self.update_dict_auto_property(prop=auto)
        inet = list(filter(lambda x: "inet" in x, stanza))
        inet6 = list(filter(lambda x: "inet6" in x, stanza))

    def update_dict_auto_property(self, prop):
        iface = prop[0].split()[1]
        self.network_interface_details[iface] = {"auto":"true"}
        print(self.network_interface_details)






def main():
    file_iterator()
    gen()


if __name__ == "__main__":
    main()


