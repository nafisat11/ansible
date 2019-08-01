import re
from collections import defaultdict
from itertools import chain

def main():
    wpa = {}
    key_list = []
    val_list = []
    
    with open("wpa_supplicant.conf", "r") as wpa_conf:
        for line in wpa_conf:
            if "#" in line:
                line = line.split("#")
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                if not 'autoscan' in key:
                    key_list.append(key)
                    val_list.append(value)
                    dup_key = [i for i, x in enumerate(key_list) if x == 'network']
                    dup_val = [i for i, x in enumerate(val_list) if x == '{']
                    dup_key.remove(0)
                    dup_val.remove(0)
                    temp1 = zip(chain([0], dup_key), chain(dup_key, [None]))
                    temp2 = zip(chain([0], dup_val), chain(dup_val, [None]))
                    new_keys = [key_list[i:j] for i, j in temp1]
                    new_vals = [val_list[i:j] for i, j in temp2]
        
        for k, v in new_keys, new_vals:
            d = tuple(k)
            s = tuple(v)
            
        print(dict(zip(d,s)))



                    





if __name__ == '__main__':
    main()