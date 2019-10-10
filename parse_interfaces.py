#!/usr/bin/python3

import sys
import os
from collections import OrderedDict
import json
import argparse
from pprint import pprint as pp
import re

class Options:
    def __init__(self):
        pass

    def parse_option(self, stanza, line):
        raise ImplementationError('Subclass needs to implement this')

class IfaceOptions(Options):
    def __init__(self):
        pass

    def parse_option(self, stanza, line):
        keywords = ["vlan-", "bridge", "wpa", "mea"]
        if not any(x in line.strip() for x in keywords):

            if line.strip().startswith("pre-up"):
                stanza.pre_up.append(line.strip().split(" ", 1)[-1])

            if line.strip().startswith("up"):
                stanza.up.append(line.strip().split(" ", 1)[-1])

            if line.strip().startswith("post-up"):
                stanza.post_up.append(line.strip().split(" ", 1)[-1])

            if line.strip().startswith("down"):
                stanza.down.append(line.strip().split(" ", 1)[-1])

            if line.strip().startswith("pre-down"):
                stanza.pre_down.append(line.strip().split(" ", 1)[-1])

            if line.strip().startswith("post-down"):
                stanza.post_down.append(line.strip().split(" ", 1)[-1])


class IPAddressOptions(Options):
    def __init__(self):
        pass

    def parse_option(self, stanza, line):
        if line.strip().startswith('address'):
            stanza.address = line.strip().split()[-1]

        if line.strip().startswith('netmask'):
            stanza.netmask = line.strip().split()[-1]

        if line.strip().startswith('gateway'):
            stanza.gateway = line.strip().split()[-1]

class VlanOptions(Options):
    def __init__(self):
        pass

    def parse_option(self, stanza, line):
        if 'vlan-raw-device' in line:
            stanza.vlan_opts.append({line.strip().split()[0]:line.strip().split()[-1]})

class BridgeOptions(Options):
    def __init__(self):
        pass

    def parse_option(self, stanza, line):
        if "bridge" in line:
            stanza.bridge_opts.append({line.strip().split()[0]:line.strip().split(" ", 1)[-1]})

class WlanOptions(Options):
    def __init__(self):
        pass

    def parse_option(self, stanza, line):
        if "wpa" in line:
            stanza.wlan_opts.append({line.strip().split()[0]:line.strip().split()[-1]})

class MeaOptions(Options):
    def __init__(self):
        pass

    def parse_option(self, stanza, line):
        if "mea" in line:
            stanza.mea_opts.append({line.strip().split()[0]:line.strip().split(" ", 1)[-1]})


class InterfaceStanza:
    def __init__(self, name, family, mode):
        self.name = name
        self.family = family
        self.mode = mode
        self.auto = False
        self._lines = []
        self.address = ''
        self.netmask = ''
        self.gateway = ''
        self.pre_up = []
        self.up = []
        self.post_up = []
        self.down = []
        self.pre_down = []
        self.post_down = []
        self.vlan_opts = []
        self.bridge_opts = []
        self.wlan_opts = []
        self.mea_opts = []
        self._options = [IPAddressOptions(), IfaceOptions(), VlanOptions(), BridgeOptions(), WlanOptions(), MeaOptions()]

    def add_detail(self, line):
        #TODO  process the line for details
        for o in self._options:
            o.parse_option(self, line)

    def show(self):
        print('''
        Interface: {}
            Family: {}
            Mode: {}
            Auto: {}
            Address: {}
            Netmask: {}
            Gateway: {}
            Pre-up: {}
            Up: {}
            Post-up: {}
            Down: {}
            Pre-down: {}
            Post-down: {}
            Vlan: {}
            Bridge: {}
            Wlan: {}
            Mea: {}
        '''.format(self.name, self.family, self.mode, self.auto, self.address
        , self.netmask, self.gateway, self.pre_up, self.up, self.post_up, self.down
        , self.pre_down, self.post_down, self.vlan_opts, self.bridge_opts, self.wlan_opts
        , self.mea_opts
        ))
        for line in self._lines:
            print('    ++ {}'.format(line))

        

def is_new_stanza(line):
    if line.strip().startswith('iface '): #Each stanza must contain an iface line
        return True
    return False

def capture_addrFam_attrib(inet, inet6, line):
    inet_match = re.search(r"inet\D", line.strip())
    if line.strip().startswith("iface"):
        inet6_match = re.search(r"inet\d", line.strip())
        if not inet6_match:
            inet.append(line.strip().split()[1])
        else:
            inet6.append(line.strip().split()[1])
        return True
    return False

def capture_auto_attrib(store, line): #stores interfaces that have auto property in a list
    if line.strip().startswith('auto '):
        store.append(line.strip().split()[-1])
        return True
    return False

def is_comment_line(line):
    if line.strip().startswith('#'):
        return True
    return False


def main():
    auto_interfaces = []
    stanzas = []
    inet_interfaces = []
    inet6_interfaces = []

    # TODO use better argument parser to process file
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
    network_interface_directory = "/home/nafisa/Downloads/"
    if os.path.isfile(os.path.join(network_interface_directory, filename)):
        network_interface_filepath = os.path.realpath(
            os.path.join(network_interface_directory, filename)
        )
    else:
        print("Please enter valid network interfaces filename")
        sys.exit(1)

    with open(network_interface_filepath) as interfaces_file:
        for line in interfaces_file:
            if capture_auto_attrib(auto_interfaces, line):
                continue
            
            elif is_comment_line(line): #remove lines with comments
                continue
            elif is_new_stanza(line): #iface line
                s = InterfaceStanza(*line.split()[1:]) #populate family, mode, and iface name 
                stanzas.append(s)
            elif len(stanzas) > 0:
                stanzas[-1].add_detail(line)
            capture_addrFam_attrib(inet_interfaces, inet6_interfaces, line)



    interfaces_json_model = {}
    network_interface_details = OrderedDict()
    header = {"version": "0.0.0"}
    interfaces_json_model["header"] = header

    for iface in inet_interfaces:
        network_interface_details[iface] = {"auto":"", "addrFam":{"inet":{}}}
    for iface in inet6_interfaces:
        if iface in network_interface_details:
            network_interface_details[iface]["addrFam"].update({"inet6":{}})


    for s in stanzas:
        if s.name in auto_interfaces:
            s.auto = True

        network_interface_details[s.name].update({"auto":s.auto})

        if s.family == "inet":
            network_interface_details[s.name]["addrFam"]["inet"] = {"mode": s.mode,
                                                                    "address": s.address,
                                                                    "netmask": s.netmask,
                                                                    "gateway": s.gateway,
                                                                    "pre-up": s.pre_up,
                                                                    "up": s.up,
                                                                    "post-up": s.post_up,
                                                                    "down": s.down,
                                                                    "pre-down": s.pre_down,
                                                                    "post-down": s.post_down,
                                                                    "vlan_opts": s.vlan_opts,
                                                                    "bridge_opts": s.bridge_opts,
                                                                    "wlan_opts": s.wlan_opts,
                                                                    "mea_opts": s.mea_opts
                                                                    }
        elif s.family == "inet6":
            network_interface_details[s.name]["addrFam"]["inet6"] = {"mode":s.mode,
                                                                     "address": s.address,
                                                                     "netmask": s.netmask,
                                                                     "gateway": s.gateway,
                                                                     "pre-up": s.pre_up,
                                                                     "up": s.up,
                                                                     "post-up": s.post_up,
                                                                     "down": s.down,
                                                                     "pre-down": s.pre_down,
                                                                     "post-down": s.post_down,
                                                                     "vlan_opts": s.vlan_opts,
                                                                     "bridge_opts": s.bridge_opts,
                                                                     "wlan_opts": s.wlan_opts,
                                                                     "mea_opts": s.mea_opts}
       
    interfaces_json_model["interfaces_data"] = network_interface_details
    


    with open("test.json", "w") as json_file:
        json.dump(
            interfaces_json_model, json_file, indent=4, separators=(",", ": ")
        )


if __name__ == '__main__':
    main()
