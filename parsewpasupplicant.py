import more_itertools as m_iter
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
        d = defaultdict(list)
        globs = []
        network_keys = []
        network_vals = []
        tmp = []
        flag = 1
        for line in wpa_conf:
            if not line.strip():
                continue
            if not "#" in line:
                line = line.strip()
                if line.startswith("network"):
                    flag = 0
                elif line.startswith("}"):
                    flag = 1

                if flag and not line.startswith("}"):
                    line = tuple(line.strip().split("="))
                    globs.append(line)

                if not flag and not line.startswith("network"):
                    key = line.strip().split("=")
                    network_keys.append(key)
        #print(network_keys)
                    #network_vals.append(value)

        #network_keys[network_keys.index("psk")] = "psk_text"

        wpa = dict(tuple(globs))
        #print(wpa)
    

        dups = [i for i, x in enumerate(network_keys) if x[0] == "ssid"]
        dups.remove(0)
        keys = [tuple(network_keys[i:j]) for i, j in zip(chain([None], dups), chain(dups, [None]))]
        #vals = tuple([tuple(network_vals[i:j]) for i, j in zip(chain([None], dups), chain(dups, [None]))])

        g = globals()
        
        for i, j in zip(chain([None], dups), chain(dups, [None])):
            g['net_{0}'.format(i)] = network_keys[i:j]

        net_0 = []
        counter = 0
        for i, v in enumerate(net_None):
            if net_None[i][0].count("psk"):
                count = net_None
            #total = net_None.count()


        wpa.update(net0=dict(net_None))
        #pp(wpa)


            

        


                

def test3():
    with open("wpa_supplicant.conf") as wpa_conf:
        tmp = []
        d = defaultdict(list)
        for line in wpa_conf:
            if not line.strip():
                continue
            if not "#" in line:
                line = line.strip()
                tmp.append(line)

        dups = [i for i, x in enumerate(tmp) if "network" in x]
        key_val = [tmp[i:j] for i, j in zip(chain([0], dups), chain(dups, [None]))]
        pp(key_val)

        for i in key_val:
            for j in i:
                j = j.split("=")
                #print(j)





if __name__ == '__main__':
    #main()
    #print(list(test()))
    test2()
    #test3()