from hostapdconf.parser import HostapdConf
from collections import OrderedDict
import json

def main():
    ap_settings = {}
    with open("hostapd.conf", "r") as ap_conf:
        for line in ap_conf:
            if line.startswith("#"):
                line, comment = line.split("#", 1)
            if "=" in line: 
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                ap_settings[key] = value

    with open("parsed_hostapd.json", "w") as json_file:
        json.dump(ap_settings, json_file, indent=4, separators=(',', ': '))


if __name__ == '__main__':
    main()

