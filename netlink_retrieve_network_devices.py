from pyroute2 import IPRoute, IPDB, IW
from pyroute2.netlink import NetlinkError

ip = IPRoute()
ipdb = IPDB()
iw = IW()


def slave_interfaces():
    iface = ipdb.by_name.keys()
    for link in iface:
        kind = ipdb.interfaces[link].get("kind")
        if kind == "bridge":
            print("Slave interface(s) to device %s:" % (link))
            slave_ifaces = ipdb.interfaces[link].ports
            for port in slave_ifaces:
                print(iface[port - 1])


def parent_interfaces():
    iface = ipdb.by_name.keys()
    for dev in iface:
        kind = ipdb.interfaces[dev].get("kind")
        if kind == "vlan":
            print("Parent interfaces(s) to device %s:" % (dev))
            parent_ifaces = ipdb.interfaces[dev].link
            try:
                for parent in parent_ifaces:
                    print(iface[parent - 1])
            except TypeError:
                print(iface[parent_ifaces - 1])


def iface_type():
    iface = ipdb.by_name.keys()
    for link in iface:
        if link != "lo":
            print("\nInterface: " + link)
            IP_addr = ipdb.interfaces[link].ipaddr.ipv4

            try:
                print("IP address: " + str(IP_addr[0].get("address")))
            except (IndexError, KeyError):
                print("IP address: Null")

            MAC_addr = ipdb.interfaces[link].get("address")
            if MAC_addr == "":
                print("MAC address: Null")
            else:
                print("MAC address: " + MAC_addr)

            ifi_type = ipdb.interfaces[link].get("ifi_type")
            kind = ipdb.interfaces[link].get("kind")

            if ifi_type == 1:
                if kind is None:
                    link_index = ip.link_lookup(ifname=link)[0]
                    try:
                        iw.get_interface_by_ifindex(link_index)
                        print("Type: wlan")
                    except NetlinkError as e:
                        if e.code == 19:
                            print("Type: ethernet")
                else:
                    print("Type: " + kind)

            elif ifi_type == 280:
                print("Type: CAN")

            else:
                print("Type: unknown")


def main():
    iface_type()
    print("-" * 80)
    slave_interfaces()
    print("-" * 80)
    parent_interfaces()


if __name__ == "__main__":
    main()
