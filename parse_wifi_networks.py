import itertools
from pprint import pprint


def main():
    with open("/home/nafisa/Documents/wpa_supplicant.conf") as wpa_supplicant:
        supplicant_details = {}
        wifi_networks = []
        is_network_stanza = False

        network_details = {}

        for line in wpa_supplicant:
            line = line.strip().split('#')
            line = line[0]
            if not line.strip():
                continue
            if line.startswith("network"):
                if network_details:
                    wifi_networks.append(network_details)
                network_details = {}
                is_network_stanza = True
                continue
            elif is_network_stanza:                
                if line.endswith('}'):
                    line = line[:-1].strip()
                    is_network_stanza = False
                kv = line.split('=')
                if len(kv) > 1:
                    if kv[0] == "psk":
                        if '"' not in kv[1]:
                            kv[0] = "psk_hash"                       
                        else:
                            kv[0] = "psk_text"
                    network_details[kv[0]] = kv[1]
            elif not is_network_stanza:
                kv = line.split('=')
                if line.endswith('}'):
                    line = line[:-1].strip()
                if len(kv) > 1:
                    supplicant_details[kv[0]] = kv[1]
        supplicant_details['networks'] = wifi_networks
        pprint(supplicant_details)


if __name__ == "__main__":
    main()