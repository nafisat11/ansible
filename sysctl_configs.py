class SysctlConfig:
    def __init__(self, data):
        self.data = data

    def write_config(self):
        with open("sysctl.conf", "w") as sysctl_conf_file:
            for k, v in self.data.items():
                sysctl_conf_file.write("{} = {}\n".format(k, v))