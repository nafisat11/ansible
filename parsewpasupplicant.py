import re
from collections import OrderedDict

def confparse():
    active = {}
    inactive = {}

    f = open("wpa_supplicant.conf")
    for line in f:
        if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()

            value = value.strip() 
            if key.startswith("#"):
                key = key.strip("#")
                inactive[key] = value
            else:
                active[key] = value
    print(inactive)

    f.close()
    