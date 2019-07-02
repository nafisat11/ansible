from pyroute2 import IPRoute, IPDB, IW
from pyroute2.netlink import NetlinkError

ip = IPRoute()
ipdb = IPDB()
iw = IW()

def ip_settings():
    iface = ipdb.by_name.keys()
    for link in iface:
        kind = ipdb.interfaces[link].get("kind")
        ifi_type = ipdb.interfaces[link].get("ifi_type")

        if ifi_type == 1 and kind is None:
            link_index = ip.link_lookup(ifname=link)[0]
            try:
                iw.get_interface_by_ifindex(link_index)
            except NetlinkError as e:
                if e.code == 19:
                    IP_addr = ipdb.interfaces[link].ipaddr.ipv4
                    try:
                        print(str(ipdb.interfaces[link].ifname))
                        print("\nStatic IP: " + str(IP_addr[0].get("address")))
                        if '24' in str(IP_addr[0].get("prefixlen")):
                            print("Static Netmask: 255.255.255.0\n")
                    except (IndexError, KeyError):
                        print("IP Settings: manual")
                        print("Static IP: Null")
                        print("Static Netmask: Null\n")



def main():
    ip_settings()

if __name__ == "__main__":
    main()