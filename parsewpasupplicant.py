from itertools import chain
from pprint import pprint as pp


def main():
    with open("wpa_supplicant.conf") as wpa_conf:
        globs = []
        network_kv = []
        flag = 1
        for line in wpa_conf:
            if not line.strip():
                continue
            if "#" not in line:
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
                    network_kv.append(key)

        wpa = dict(tuple(globs))

        dups = [i for i, x in enumerate(network_kv) if x[0] == "ssid"]
        dups.remove(0)

        g = globals()

        num_of_lists = list(map(lambda x: x, range(len(dups) + 1)))
        iterator = iter(num_of_lists)

        for i, j in zip(chain([None], dups), chain(dups, [None])):
            g["net_{0}".format(next(iterator))] = network_kv[i:j]

        for i, v in enumerate(net_0):
            if net_0[i][0] == "psk":
                if '"' not in net_0[i][1]:
                    net_0[i][0] = "psk_hash"
                else:
                    net_0[i][0] = "psk_text"

        for i, v in enumerate(net_1):
            if net_1[i][0] == "psk":
                if '"' not in net_1[i][1]:
                    net_1[i][0] = "psk_hash"
                else:
                    net_1[i][0] = "psk_text"

        for i, v in enumerate(net_2):
            if net_2[i][0] == "psk":
                if '"' not in net_2[i][1]:
                    net_2[i][0] = "psk_hash"
                else:
                    net_2[i][0] = "psk_text"

        for i, v in enumerate(net_3):
            if net_3[i][0] == "psk":
                if '"' not in net_3[i][1]:
                    net_3[i][0] = "psk_hash"
                else:
                    net_3[i][0] = "psk_text"

        net = [dict(net_0), dict(net_1), dict(net_2), dict(net_3)]

        wpa.update(network=net)
        pp(wpa)


if __name__ == "__main__":
    main()
