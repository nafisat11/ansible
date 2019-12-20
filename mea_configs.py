class MeaConfig:
    def __init__(self, data):
        self.data = data
        self.interface = self.data["interface"]

    def write_config(self):
        with open("{}.conf".format(self.interface), "w") as mea_conf_file:
            for k, v in self.data.items():
                if k == "interface" or v is "":
                    continue
                mea_conf_file.write("imconfig {} {} {}\n".format(self.interface, k, v))
