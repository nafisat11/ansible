import re
import argparse
import os
import sys
import json
import socket
from collections import OrderedDict

class Iface_Parse_FSM:
    def __init__(self, filename):
        self.filename = filename
        self.current_state = None
        self.next_state = None
        self.prev_state = None
        self.iter = 1
        self.current_iface = None
        self.lines_in_file = []
        self.max_iter = None
        self.interfaces_json_model = {}
        self.network_interface_details = OrderedDict()

    def run(self):
        with open(self.filename) as interfaces_file:
            for line in interfaces_file:
                line = line.strip().split("#")[0]
                if not line.strip():
                    continue
                self.lines_in_file.append(line)
        self.max_iter = len(self.lines_in_file)      
        self.iterate_through_lines(self.iter)


    def iterate_through_lines(self, next_position):
        self.next_position = next_position
        self.next_state = self.read_line(self.lines_in_file[self.next_position])


    def read_line(self, line):
        if "auto" in line:
            self.next_state = self.auto_state(line)

        elif "iface" in line:
            self.next_state = self.iface_state(line)

        elif self.current_state == "iface_state" and self.prev_state == "auto_state":
            self.next_state = self.iface_details_state(line)

        elif self.current_state == "iface_state" and self.prev_state == "iface_details_state":
            self.next_state == self.iface_details_state(line)

        elif self.current_state == "iface_state" and self.prev_state == "iface_state":
            self.next_state = self.iface_details_state(line)
 
        elif self.current_state == "iface_details_state" and self.prev_state == "iface_state":
            self.next_state = self.iface_details_state(line)

        elif self.current_state == "iface_details_state" and self.prev_state == "iface_details_state":
            self.next_state == self.iface_details_state(line)

        elif self.current_state == "auto_state" and self.prev_state == "iface_details_state":
            self.next_state == self.auto_state(line)


    def auto_state(self, line):
        self.prev_state = self.current_state
        self.current_state = "auto_state"
        auto_line = line.split()
        if auto_line[1] == self.current_iface:
            pass
        else:
            self.current_iface = auto_line[1]
            self.network_interface_details[self.current_iface] = {"auto":"true"} #actually updates

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
            #actually updates
            if "inet" in iface_line:
                self.network_interface_details[self.current_iface].update({"inet":{}})
                self.network_interface_details[self.current_iface]["inet"].update({"mode":iface_line[3]})
            elif "inet6" in iface_line:
                self.network_interface_details[self.current_iface].update({"inet6":{}})
                self.network_interface_details[self.current_iface]["inet6"].update({"mode":iface_line[3]})

        else:
            self.current_iface = iface_line[1]
            if iface_line[1] in self.network_interface_details:
                pass
            else:
                self.network_interface_details[self.current_iface] = {"auto":"false"} #actually updates
                if "inet" in iface_line:
                    self.network_interface_details[self.current_iface].update({"inet":{}})
                    self.network_interface_details[self.current_iface]["inet"].update({"mode":iface_line[3]})

                elif "inet6" in iface_line:
                    self.network_interface_details[self.current_iface].update({"inet6":{}})
                    self.network_interface_details[self.current_iface]["inet6"].update({"mode":iface_line[3]})

        self.iter += 1
        if self.iter != self.max_iter:
            self.next_state = self.iterate_through_lines(self.iter)
        else:
            self.next_state = self.all_lines_read()

    def iface_details_state(self, line):
        self.prev_state = self.current_state
        self.current_state = "iface_details_state"
        iface_detail_line = line.split()

        if "address" in line:
            ip_match = re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", iface_detail_line[1])
            if ip_match:
                self.network_interface_details[self.current_iface]["inet"].update({"address":iface_detail_line[1]})
            else:
                self.network_interface_details[self.current_iface]["inet6"].update({"address":iface_detail_line[1]})

        if "netmask" in line:
            if "64" in line:
                self.network_interface_details[self.current_iface]["inet6"].update({"netmask":iface_detail_line[1]})
            else:
                self.network_interface_details[self.current_iface]["inet"].update({"netmask":iface_detail_line[1]})

        if "gateway" in line:
            self.network_interface_details[self.current_iface]["inet"].update({"gateway":iface_detail_line[1]})

        if "broadcast" in line:
            self.network_interface_details[self.current_iface]["inet"].update({"broadcast":iface_detail_line[1]})

        if self.current_iface == "wlan0":
            print(line)



        self.iter += 1
        if self.iter != (self.max_iter):
            self.next_state = self.iterate_through_lines(self.iter)
        else:
            self.next_state = self.all_lines_read()

    def all_lines_read(self):
        print("finished iterating through all lines")
        header = {"version":"0.0.0"}
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

if __name__ == '__main__':
    main()