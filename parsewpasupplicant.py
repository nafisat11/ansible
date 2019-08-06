import re
from collections import defaultdict
from itertools import chain
from pprint import pprint as pp


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
                #key_list.append(key)
                #val_list.append(value)

                key_list.append(key)
                val_list.append(value)
                dup_key = [i for i, x in enumerate(key_list) if x == 'network']
                dup_val = [i for i, x in enumerate(val_list) if x == '{']
                temp1 = zip(chain([0], dup_key), chain(dup_key, [None]))
                temp2 = zip(chain([0], dup_val), chain(dup_val, [None]))
                new_keys = [key_list[i:j] for i, j in temp1]
                new_vals = [val_list[i:j] for i, j in temp2]
    
        print(list(zip(new_keys,new_vals)))

def test():
    with open("wpa_supplicant.conf") as wpa_conf:
        vals = ("autoscan", "network", " ")
        tmp = []
        for line in wpa_conf:
            line = line.strip()
            if line.startswith(vals):
                yield tmp
                tmp = [line]
            else:
                if not "#" in line:
                    line = line.lstrip()                  
                    tmp.append(line)

    if tmp:
        yield tmp

def test2():
    with open("wpa_supplicant.conf") as wpa_conf, open("output.txt", "w+") as outfile:
        tmp = []
        for line in wpa_conf:
            vals = ("autoscan", "network", " ")
            if line.startswith(vals):
                if not line.strip():
                    continue
                if not "#" in line:
                    line = line.strip()
                    tmp.append(line)
        pp(tmp)

def test3():
    with open("wpa_supplicant.conf") as wpa_conf:
        tmp = []
        for line in wpa_conf:
            if not line.strip():
                continue
            if not "#" in line:
                line = line.strip()
                tmp.append(line)

        dups = [i for i, x in enumerate(tmp) if "network" in x]
        key_val = [tmp[i:j] for i, j in zip(chain([0], dups), chain(dups, [None]))]
        pp(key_val)
        #pp(ds)
        #print(tmp[dups[2]:])





if __name__ == '__main__':
    #main()
    #print(list(test()))
    #test2()
    test3()