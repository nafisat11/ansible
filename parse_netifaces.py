import debinterface
from pprint import pprint as pp
import json
from collections import OrderedDict


def main():
    netiface = OrderedDict()
    ifaces = []
    names = []
    iface_info = []
    interfaces = debinterface.Interfaces(interfaces_path="/home/nafisa/Documents/iface")
    adapters = interfaces.adapters

    for ad in adapters:
        item = ad.export()
        ifaces.append(item)
        names.append(ad.attributes["name"])

    for index, iface in enumerate(ifaces):
        iface_info.append(
            {
                "addrFam": iface.get("addrFam", None),
                "auto": iface.get("auto", None),
                "ip setting": iface.get("source", None),
                "address": iface.get("address", None),
                "netmask": iface.get("netmask", None),
                "gateway": iface.get("gateway", None),
                "up": iface.get("up", None),
                "down": iface.get("down", None),
                "pre-up": iface.get("pre-up", None),
                "pre-down": iface.get("pre-down", None),
                "post-up": iface.get("post-up", None),
                "post-down": iface.get("post-down", None),
                "bridge-opts": iface.get("bridge-opts", None),
                "wlan-opts": iface.get("unknown", None),
            }
        )

    for key, value in zip(names, iface_info):
        netiface.setdefault(key, []).append(value)

    with open("parsed_network_interfaces.json", "w") as json_file:
        json.dump(netiface, json_file, indent=4, separators=(",", ": "), sort_keys=True)


if __name__ == "__main__":
    main()
