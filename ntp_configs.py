class NtpConfig:
    def __init__(self, data):
        self.data = data

    def write_config(self):
        with open("ntp.conf", "w") as ntp_conf_file:
            for k, v in self.data.items():
                if v is "" or v is None:
                    continue
                ntp_conf_file.write("{} = {}\n".format(k, v))
