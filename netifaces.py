import re
import argparse
import os
import sys
import json
import itertools
from collections import OrderedDict


class Iface_Parse_FSM:
    interfaces_json_model = {}
    network_interface_details = OrderedDict()
    wlan_opts = {}
    bridge_opts = {}
    vlan_opts = {}
    mea_opts = OrderedDict()

    def __init__(self, filename):
        self.filename = filename
        self.current_state = None
        self.next_state = None
        self.prev_state = None
        self.iter = 1
        self.prev_iface = None
        self.current_iface = None
        self.lines_in_file = []
        self.max_iter = None
        self.inet_iface = None
        self.inet6_iface = None

    def run(self):
        with open(self.filename) as interfaces_file:
            for line in interfaces_file:
                line = line.strip().split("#")[0]
                if not line.strip():
                    continue
                self.lines_in_file.append(line)
        self.max_iter = len(self.lines_in_file)
        self.iterate_through_lines(self.iter)

    def iterate_through_lines(self, next_line):
        self.next_line = next_line
        self.next_state = self.read_line(self.lines_in_file[self.next_line])

    def read_line(self, line):
        if "auto" in line:
            self.next_state = self.auto_state(line)

        elif "iface" in line:
            self.next_state = self.iface_state(line)

        elif self.current_state == "iface_state" and self.prev_state == "auto_state":
            self.next_state = self.iface_details_state(line)

        elif (
            self.current_state == "iface_state"
            and self.prev_state == "iface_details_state"
        ):
            self.next_state == self.iface_details_state(line)

        elif self.current_state == "iface_state" and self.prev_state == "iface_state":
            self.next_state = self.iface_details_state(line)

        elif (
            self.current_state == "iface_details_state"
            and self.prev_state == "iface_state"
        ):
            self.next_state = self.iface_details_state(line)

        elif (
            self.current_state == "iface_details_state"
            and self.prev_state == "iface_details_state"
        ):
            self.next_state == self.iface_details_state(line)

        elif (
            self.current_state == "auto_state"
            and self.prev_state == "iface_details_state"
        ):
            self.next_state == self.auto_state(line)

    def auto_state(self, line):
        self.prev_state = self.current_state
        self.current_state = "auto_state"
        auto_line = line.split()
        if auto_line[1] == self.current_iface:
            pass
        else:
            self.current_iface = auto_line[1]
            self.network_interface_details[self.current_iface] = {
                "auto": "true", "addrFam":{}
            }  # actually updates

        self.iter += 1
        if self.iter != self.max_iter:
            self.next_state = self.iterate_through_lines(self.iter)
        else:
            self.next_state = self.all_lines_read()

    def iface_state(self, line):
        self.prev_state = self.current_state
        self.current_state = "iface_state"
        iface_line = line.split()

        if iface_line[1] == self.current_iface:
            # actually updates
            if "inet" in iface_line:
                self.inet_iface = True
                self.inet6_iface = False
                self.network_interface_details[self.current_iface]["addrFam"].update({"inet": {}})
                self.network_interface_details[self.current_iface]["addrFam"]["inet"].update(
                    {"mode": iface_line[3]}
                )
            elif "inet6" in iface_line:
                self.inet6_iface = True
                self.inet_iface = False
                self.network_interface_details[self.current_iface]["addrFam"].update({"inet6": {}})
                self.network_interface_details[self.current_iface]["addrFam"]["inet6"].update(
                    {"mode": iface_line[3]}
                )

        else:
            self.current_iface = iface_line[1]
            if iface_line[1] in self.network_interface_details:
                pass
            else:
                self.network_interface_details[self.current_iface] = {
                    "auto": "false", "addrFam":{}
                }  # actually updates
                if "inet" in iface_line:
                    self.inet_iface = True
                    self.inet6_iface = False
                    self.network_interface_details[self.current_iface]["addrFam"].update(
                        {"inet": {}}
                    )
                    self.network_interface_details[self.current_iface]["addrFam"]["inet"].update(
                        {"mode": iface_line[3]}
                    )

                elif "inet6" in iface_line:
                    self.inet6_iface = True
                    self.inet_iface = False
                    self.network_interface_details[self.current_iface]["addrFam"].update(
                        {"inet6": {}}
                    )
                    self.network_interface_details[self.current_iface]["addrFam"]["inet6"].update(
                        {"mode": iface_line[3]}
                    )

        self.iter += 1
        if self.iter != self.max_iter:
            self.next_state = self.iterate_through_lines(self.iter)
        else:
            self.next_state = self.all_lines_read()

    def iface_details_state(self, line):
        self.prev_state = self.current_state
        self.current_state = "iface_details_state"
        iface_detail_line = line.split(" ", 1)
        
        if self.inet_iface and not self.inet6_iface:

            if "wpa" in line:
                self.network_interface_details[self.current_iface]["addrFam"]["inet"].update(
                    {"wlan_opts": {iface_detail_line[0]:iface_detail_line[1]}}
                )

            elif "vlan" in line:
                self.vlan_opts.setdefault(iface_detail_line[0], []).append(
                    iface_detail_line[1]
                )
                self.network_interface_details[self.current_iface]["addrFam"]["inet"].update(
                    {"vlan_opts": self.vlan_opts}
                )

                print(self.vlan_opts)

            elif "bridge" in line:
                self.bridge_opts[iface_detail_line[0]] = iface_detail_line[1]
                self.network_interface_details[self.current_iface]["addrFam"]["inet"].update(
                    {"bridge_opts": self.bridge_opts}
                )

            elif "mea" in line:
                self.mea_opts[iface_detail_line[0]] = iface_detail_line[1]
                self.network_interface_details[self.current_iface]["addrFam"]["inet"].update(
                    {"mea_opts": self.mea_opts}
                )

            else:
                self.network_interface_details[self.current_iface]["addrFam"]["inet"].update(
                    {iface_detail_line[0]: iface_detail_line[1]}
                )

        elif self.inet6_iface and not self.inet_iface:
            if "wpa" in line:
                self.wlan_opts[iface_detail_line[0]] = iface_detail_line[1]
                self.network_interface_details[self.current_iface]["addrFam"]["inet6"].update(
                    {"wlan_opts": self.wlan_opts}
                )

            elif "vlan" in line:
                self.vlan_opts[iface_detail_line[0]] = iface_detail_line[1]
                self.network_interface_details[self.current_iface]["addrFam"]["inet6"].update(
                    {"vlan_opts": self.vlan_opts}
                )

            elif "bridge" in line:
                self.bridge_opts[iface_detail_line[0]] = iface_detail_line[1]
                self.network_interface_details[self.current_iface]["addrFam"]["inet6"].update(
                    {"bridge_opts": self.bridge_opts}
                )

            elif "mea" in line:
                self.mea_opts.setdefault(iface_detail_line[0], []).append(
                    iface_detail_line[1]
                )
                self.network_interface_details[self.current_iface]["addrFam"]["inet6"].update(
                    {"mea_opts": self.mea_opts}
                )

            else:
                self.network_interface_details[self.current_iface]["addrFam"]["inet6"].update(
                    {iface_detail_line[0]: iface_detail_line[1]}
                )

        self.iter += 1
        if self.iter != (self.max_iter):
            self.next_state = self.iterate_through_lines(self.iter)
        else:
            self.next_state = self.all_lines_read()

    def populate_details(self):
        pass

    def all_lines_read(self):
        header = {"version": "0.0.0"}
        self.interfaces_json_model["header"] = header
        self.interfaces_json_model["interfaces_data"] = self.network_interface_details

        with open("parsed_network_interfaces.json", "w") as json_file:
            json.dump(
                self.interfaces_json_model, json_file, indent=4, separators=(",", ": ")
            )


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

    fsm = Iface_Parse_FSM(network_interface_filepath)
    fsm.run()


if __name__ == "__main__":
    main()
