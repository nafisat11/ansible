import json
import argparse
import os


class RajantConfig:
    def __init__(self, data):
        self.bc_data = data

    def add_line(self, line):
        with open("{}.conf".format(self.bc_data["serial"]), "a+") as bc_conf_file:
            for line_found in bc_conf_file:
                if line in line_found:
                    break
            else:
                bc_conf_file.write(line)

    def assignment_setting(self):
        self.add_line(
            "bcconfig set --assignment={}\n".format(self.bc_data.get("assignment"))
        )

    def ip_setting(self):
        self.add_line("bcconfig set --ip {}\n".format(self.bc_data.get("ip")))

    def netmask_setting(self):
        self.add_line("bcconfig set --netmask {}\n".format(self.bc_data.get("netmask")))

    def gateway_setting(self):
        self.add_line("bcconfig set --gateway {}\n".format(self.bc_data.get("gateway")))

    def dns_setting(self):
        self.add_line("bcconfig set --dns {}\n".format(self.bc_data.get("dns")))

    def netkey_setting(self):
        self.add_line("bcconfig set --netkey {}\n".format(self.bc_data.get("netkey")))

    def netname_setting(self):
        self.add_line("bcconfig set --netname {}\n".format(self.bc_data.get("netname")))

    def security_setting(self):  # ??
        pass

    def bandwith_setting(self):
        for k, v in self.bc_data.get("bandwith").items():
            for iface, bandwith in v.items():
                self.add_line("bcconfig set --bandwith={} {}\n".format(iface, bandwith))

    def channel_setting(self):
        for k, v in self.bc_data.get("channel").items():
            for iface, channel in v.items():
                self.add_line("bcconfig set --channel={} {}\n".format(iface, channel))

    def powerlevel_setting(self):
        for k, v in self.bc_data.get("powerlevel").items():
            for iface, powerlevel in v.items():
                self.add_line(
                    "bcconfig set --powerlevel={} {}\n".format(iface, powerlevel)
                )

    def regmode_setting(self):
        for k, v in self.bc_data.get("regmode").items():
            for iface, mode in v.items():
                self.add_line("bcconfig set --bandwith={} {}\n".format(iface, mode))

    def gpsip_setting(self):
        self.add_line("bcconfig set --gpsip {}\n".format(self.bc_data.get("gpsip")))

    def gpsport_setting(self):
        self.add_line("bcconfig set --gpsport {}\n".format(self.bc_data.get("gpsport")))

    bc_settings = {
        "assignment": assignment_setting,
        "ip": ip_setting,
        "netmask": netmask_setting,
        "gateway": gateway_setting,
        "dns": dns_setting,
        "netkey": netkey_setting,
        "netname": netname_setting,
        # "security": self.bc_data.get("security"),
        "bandwith": bandwith_setting,
        "channel": channel_setting,
        "powerlevel": powerlevel_setting,
        "regmode": regmode_setting,
        "gpsip": gpsip_setting,
        "gpsport": gpsport_setting,
    }

    def get_setting(self):
        for setting in self.bc_settings:
            if self.bc_data[setting] is "" or self.bc_data[setting] is None:
                continue
            self.bc_settings[setting].__get__(self)()


class InterfacesConfig:
    def __init__(self, data, iface):
        self.data = data
        self.iface = iface


class ListProps(InterfacesConfig):
    def get_property(self):
        pass

    def add_line(self):
        for k, v in self.get_properties().items():
            with open("{}.conf".format(self.iface), "a") as iface_conf_file:
                if not v or v is None:
                    continue
                for opt in range(len(v)):
                    iface_conf_file.write("    {} {}\n".format(k, v[opt]))


class StringProps(InterfacesConfig):
    def get_property(self):
        pass

    def add_line(self):
        for k, v in self.get_properties().items():
            with open("{}.conf".format(self.iface), "a") as iface_conf_file:
                if v is "" or v is None:
                    continue
                iface_conf_file.write("    {} {}\n".format(k, v))


class DictProps(InterfacesConfig):
    def get_property(self):
        pass

    def add_line(self):
        for opt, value in self.get_properties().items():
            with open(
                "{}.conf".format(self.iface), "a"
            ) as iface_conf_file:  # if not v or v is None
                if type(value) is list:
                    iface_conf_file.write("    {} {}\n".format(opt, " ".join(value)))
                else:
                    iface_conf_file.write("    {} {}\n".format(opt, value))


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
            ip6MeaOpts(self.data, self.iface).add_line()


class ip4addr_props(StringProps):
    def get_properties(self):
        address = self.data[self.iface]["addrFam"]["inet"].get("address")
        netmask = self.data[self.iface]["addrFam"]["inet"].get("netmask")
        gateway = self.data[self.iface]["addrFam"]["inet"].get("gateway")

        return {"address": address, "netmask": netmask, "gateway": gateway}


class ip6addr_props(StringProps):
    def get_properties(self):
        address = self.data[self.iface]["addrFam"]["inet6"].get("address")
        netmask = self.data[self.iface]["addrFam"]["inet6"].get("netmask")
        gateway = self.data[self.iface]["addrFam"]["inet6"].get("gateway")

        return {"address": address, "netmask": netmask, "gateway": gateway}


class ip4IfaceOptions(ListProps):
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


class ip6IfaceOptions(ListProps):
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


class ip4VlanOpts(DictProps):
    def get_properties(self):
        pass


class ip6VlanOpts(DictProps):
    def get_properties(self):
        pass


class ip4BridgeOpts(DictProps):
    def get_properties(self):
        return self.data[self.iface]["addrFam"]["inet"].get("bridge_opts")


class ip6BridgeOpts(DictProps):
    def get_properties(self):
        return self.data[self.iface]["addrFam"]["inet6"].get("bridge_opts")


class ip4WlanOpts(DictProps):
    def get_properties(self):
        return self.data[self.iface]["addrFam"]["inet"].get("wlan_opts")


class ip6WlanOpts(DictProps):
    def get_properties(self):
        return self.data[self.iface]["addrFam"]["inet6"].get("wlan_opts")


class ip4MeaOpts(ListProps):
    def get_properties(self):
        return self.data[self.iface]["addrFam"]["inet"].get("mea_opts")


class ip6MeaOpts(ListProps):
    def get_properties(self):
        return self.data[self.iface]["addrFam"]["inet6"].get("mea_opts")


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
        rajant_data = data_structure["data"]["rajant"]
        for iface in interfaces_data.keys():
            auto_prop(interfaces_data, iface).add_line()
            addrFam(interfaces_data, iface).add_line()

        for breadcrumb in rajant_data["breadcrumbs"]:
            RajantConfig(breadcrumb).get_setting()


if __name__ == "__main__":
    main()
