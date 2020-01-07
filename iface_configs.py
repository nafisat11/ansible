class ifaceDetails:
    def __init__(self, data):
        self.stringOpts = {
            "address": data.get("address", ""),
            "netmask": data.get("netmask", ""),
            "gateway": data.get("gateway", ""),
        }

        self.listOpts = {
            "pre-up": data.get("pre-up", []),
            "up": data.get("up", []),
            "post-up": data.get("post-up", []),
            "pre-down": data.get("pre-down", []),
            "down": data.get("down", []),
            "post-down": data.get("post-down", []),
        }

        self.dictOpts = [                              
            data.get("vlan_opts", {}),
            data.get("bridge_opts", {}),
            data.get("wlan_opts", {}),
            data.get("wlan_opts", {}),
            data.get("mea_opts", {})
        ]

        self.iface_details = []

    def details(self):
        for k, v in self.stringOpts.items():
            if v == "":
                continue
            self.iface_details.append("    {} {}\n".format(k, v))

        for k, v in self.listOpts.items():
            if not v:
                continue
            for opt in range(len(v)):
                self.iface_details.append("    {} {}\n".format(k, v[opt]))

        for opt in self.dictOpts:
            for k, v in opt.items():
                if type(v) is list:
                    self.iface_details.append("    {} {}\n".format(k, " ".join(v)))
                elif type(v) is dict:
                    if k == "vlan-raw-device":
                        self.iface_details.append(
                            "    {} {}\n".format(k, v.get("parent"))
                        )
                else:
                    self.iface_details.append("    {} {}\n".format(k, v))

        return self.iface_details
