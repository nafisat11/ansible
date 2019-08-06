from hostapdconf.parser import HostapdConf
from collections import OrderedDict

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
        
        ordered = OrderedDict(ap_settings) 
    
    print(ordered)



if __name__ == '__main__':
    main()

