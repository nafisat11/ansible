class WpaSupplicantConfig:
    def __init__(self, data):
        self.data = data

    def add_line(self, line):
        with open(
            "wpa_supplicant.{}.conf".format(self.data["interface"]), "a+"
        ) as wpa_supplicant_file:
            wpa_supplicant_file.write(line)

    def get_global_props(self):
        for k, v in self.data.items():
            if k == "interface" or k == "networks":
                continue
            self.add_line("{}={}\n\n".format(k, v))

    def get_network_props(self):
        for network in self.data["networks"]:
            self.add_line("network={\n")
            for k, v in network.items():
                if v is "" or v is None:
                    continue
                self.add_line("    {}={}\n".format(k, v))
            self.add_line("}\n\n")

    def write_config(self):
        self.get_global_props()
        self.get_network_props()
