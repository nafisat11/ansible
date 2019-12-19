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
