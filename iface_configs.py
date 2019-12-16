import json
import argparse
import os


class InterfacesConfig:
    def __init__(self, data, iface):
        self.data = data
        self.iface = iface

class auto_prop(InterfacesConfig):
    def get_property(self):
        return self.data[self.iface].get("auto")

    def add_line(self):
        if self.get_property():
            with open("{}.conf".format(self.iface), "w") as iface_conf_file:
                iface_conf_file.write("auto {}\n".format(self.iface))


class addrFam(InterfacesConfig):
    def get_inet_property(self):
        return self.data[self.iface]["addrFam"].get("inet")

    def get_inet6_property(self):
        return self.data[self.iface]["addrFam"].get("inet6")

    def add_line(self):
        if self.get_inet_property():
            with open("{}.conf".format(self.iface), "a") as iface_conf_file:
                iface_conf_file.write(
                    "iface {} inet {}\n".format(
                        self.iface, self.data[self.iface]["addrFam"]["inet"].get("mode")
                    )
                )
            ip4addr_props(self.data, self.iface).add_line()
            ip4IfaceOptions(self.data, self.iface).add_line()
            ip4BridgeOpts(self.data, self.iface).add_line()
            ip4WlanOpts(self.data, self.iface).add_line()
            ip4MeaOpts(self.data, self.iface).add_line()

        if self.get_inet6_property():
            with open("{}.conf".format(self.iface), "a") as iface_conf_file:
                iface_conf_file.write(
                    "\niface {} inet6 {}\n".format(
                        self.iface,
                        self.data[self.iface]["addrFam"]["inet6"].get("mode"),
                    )
                )
            ip6addr_props(self.data, self.iface).add_line()
            ip6IfaceOptions(self.data, self.iface).add_line()
            ip6BridgeOpts(self.data, self.iface).add_line()
            ip6WlanOpts(self.data, self.iface).add_line()


class ip4addr_props(InterfacesConfig):
    def get_properties(self):
        address = self.data[self.iface]["addrFam"]["inet"].get("address")
        netmask = self.data[self.iface]["addrFam"]["inet"].get("netmask")
        gateway = self.data[self.iface]["addrFam"]["inet"].get("gateway")

        return {"address": address, "netmask": netmask, "gateway": gateway}

    def add_line(self):
        for k, v in self.get_properties().items():
            with open("{}.conf".format(self.iface), "a") as iface_conf_file:
                if v is "" or v is None:
                    continue
                iface_conf_file.write("    {} {}\n".format(k, v))


class ip6addr_props(InterfacesConfig):
    def get_properties(self):
        address = self.data[self.iface]["addrFam"]["inet6"].get("address")
        netmask = self.data[self.iface]["addrFam"]["inet6"].get("netmask")
        gateway = self.data[self.iface]["addrFam"]["inet6"].get("gateway")

        return {"address": address, "netmask": netmask, "gateway": gateway}

    def add_line(self):
        for k, v in self.get_properties().items():
            with open("{}.conf".format(self.iface), "a") as iface_conf_file:
                if v is "" or v is None:
                    continue
                iface_conf_file.write("    {} {}\n".format(k, v))


class ip4IfaceOptions(ip4addr_props):
    def get_properties(self):
        pre_up = self.data[self.iface]["addrFam"]["inet"].get("pre-up")
        up = self.data[self.iface]["addrFam"]["inet"].get("up")
        post_up = self.data[self.iface]["addrFam"]["inet"].get("post-up")
        pre_down = self.data[self.iface]["addrFam"]["inet"].get("pre-down")
        down = self.data[self.iface]["addrFam"]["inet"].get("down")
        post_down = self.data[self.iface]["addrFam"]["inet"].get("post-down")

        return {
            "pre-up": pre_up,
            "up": up,
            "post-up": post_up,
            "pre-down": pre_down,
            "down": down,
            "post-down": post_down,
        }

    def add_line(self):
        for k, v in self.get_properties().items():
            with open("{}.conf".format(self.iface), "a") as iface_conf_file:
                if not v or v is None:
                    continue
                for opt in range(len(v)):
                    iface_conf_file.write("    {} {}\n".format(k, v[opt]))


class ip6IfaceOptions(ip6addr_props):
    def get_properties(self):
        pre_up = self.data[self.iface]["addrFam"]["inet6"].get("pre-up")
        up = self.data[self.iface]["addrFam"]["inet6"].get("up")
        post_up = self.data[self.iface]["addrFam"]["inet6"].get("post-up")
        pre_down = self.data[self.iface]["addrFam"]["inet6"].get("pre-down")
        down = self.data[self.iface]["addrFam"]["inet6"].get("down")
        post_down = self.data[self.iface]["addrFam"]["inet6"].get("post-down")

        return {
            "pre-up": pre_up,
            "up": up,
            "post-up": post_up,
            "pre-down": pre_down,
            "down": down,
            "post-down": post_down,
        }

    def add_line(self):
        for k, v in self.get_properties().items():
            with open("{}.conf".format(self.iface), "a") as iface_conf_file:
                if not v or v is None:
                    continue
                for opt in range(len(v)):
                    iface_conf_file.write("    {} {}\n".format(k, v[opt]))


class ip4VlanOpts(ip4addr_props):
    def get_properties(self):
        pass

    def add_line(self):
        pass


class ip6VlanOpts(ip6addr_props):
    def get_properties(self):
        pass

    def add_line(self):
        pass


class ip4BridgeOpts(ip4addr_props):
    def get_properties(self):
        return self.data[self.iface]["addrFam"]["inet"].get("bridge_opts")

    def add_line(self):
        for opt, value in self.get_properties().items():
            with open(
                "{}.conf".format(self.iface), "a"
            ) as iface_conf_file:  # if not v or v is None
                if type(value) is list:
                    iface_conf_file.write("    {} {}\n".format(opt, " ".join(value)))
                else:
                    iface_conf_file.write("    {} {}\n".format(opt, value))


class ip6BridgeOpts(ip6addr_props):
    def get_properties(self):
        return self.data[self.iface]["addrFam"]["inet6"].get("bridge_opts")

    def add_line(self):
        for opt, value in self.get_properties().items():
            with open("{}.conf".format(self.iface), "a") as iface_conf_file:
                if type(value) is list:
                    iface_conf_file.write("    {} {}\n".format(opt, " ".join(value)))
                else:
                    iface_conf_file.write("    {} {}\n".format(opt, value))


class ip4WlanOpts(ip4addr_props):
    def get_properties(self):
        return self.data[self.iface]["addrFam"]["inet"].get("wlan_opts")

    # def add_line(self):
    #    for opt, value in self.get_properties().items():
    #        with open("{}.conf".format(self.iface), "a") as iface_conf_file:
    #            iface_conf_file.write("    {} {}\n".format(opt, value))


class ip6WlanOpts(ip6addr_props):
    def get_properties(self):
        return self.data[self.iface]["addrFam"]["inet6"].get("wlan_opts")


class ip4MeaOpts(ip4addr_props):
    def get_properties(self):
        return self.data[self.iface]["addrFam"]["inet"].get("mea_opts")

    def add_line(self):
        for k, v in self.get_properties().items():
            with open("{}.conf".format(self.iface), "a") as iface_conf_file:
                if not v or v is None:
                    continue
                for opt in range(len(v)):
                    iface_conf_file.write("    {} {}\n".format(k, v[opt]))


class ip6MeaOpts(ip6addr_props):
    def get_properties(self):
        return self.data[self.iface]["addrFam"]["inet6"].get("mea_opts")

    def add_line(self):
        pass


def main():
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
        for iface in interfaces_data.keys():
            with open("{}.conf".format(iface), "w") as iface_conf_file:
                auto_prop(interfaces_data, iface).add_line()
                addrFam(interfaces_data, iface).add_line()


if __name__ == "__main__":
    main()
