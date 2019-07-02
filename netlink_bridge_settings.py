from pyroute2 import IPRoute, IPDB

ip = IPRoute()
ipdb = IPDB()

def ip_settings():
    iface = ipdb.by_name.keys()
    for link in iface:
        kind = ipdb.interfaces[link].get("kind")
        if kind == "bridge":
            print(link)
            print("Interfaces to Bridge %s:" % (link))
            slave_ifaces = ipdb.interfaces[link].ports
            for port in slave_ifaces:
                print(iface[port - 1])

            IP_addr = ipdb.interfaces[link].ipaddr.ipv4

            try:
                print("\nStatic IP: " + str(IP_addr[0].get("address")))
                if '24' in str(IP_addr[0].get("prefixlen")):
                    print("Static Netmask: 255.255.255.0")
            except (IndexError, KeyError):
                print("IP Settings: manual")
                print("IP address: Null")


def main():
    ip_settings()

if __name__ == "__main__":
    main()