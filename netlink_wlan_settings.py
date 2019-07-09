from pyroute2 import IPRoute, IPDB, IW
import subprocess

ip = IPRoute()
ipdb = IPDB()
iw = IW()

#def general_settings():

def iface_type():
    iface = ipdb.by_name.keys()
    for dev in iface:
        if dev in iw.get_interfaces_dict().keys():

            cmd = """sudo iw dev %s info | grep txpower | sed 's/txpower*//'""" % (dev)
            cmd2 = """sudo iw dev %s info | grep channel | sed 's/channel*//' | cut -f1 -d'('""" % (dev)
            p = subprocess.Popen((cmd), shell=True, stdout=subprocess.PIPE)
            p2 = subprocess.Popen((cmd2), shell=True, stdout=subprocess.PIPE)
            output = p.communicate()[0].strip().decode("utf-8")
            output2 = p2.communicate()[0].strip().decode("utf-8")

            print("Maximum Transmit Power: " + output)

            link_index = ip.link_lookup(ifname=dev)[0]
            attributes = dict(iw.get_interface_by_ifindex(link_index)[0].get("attrs"))
            print(attributes.get("NL80211_ATTR_IFTYPE"))
            if attributes.get("NL80211_ATTR_IFTYPE") == 2:
                print("Interface Type: subscriber")
                print("SSID:", attributes.get("NL80211_ATTR_SSID"))
                print("Channel:", output2)

            else:
                print("Interface Type: access-point")
                print("SSID:", attributes.get("NL80211_ATTR_SSID"))

            
def ip_settings():
    iface = ipdb.by_name.keys()
    for dev in iface:
        if dev in iw.get_interfaces_dict().keys():
            link_index = ip.link_lookup(ifname=dev)[0]
            
            cmd = """cat /var/lib/dhcp/dhclient.leases | grep %s""" % (dev)
            p = subprocess.Popen((cmd), shell=True, stdout=subprocess.PIPE)
            output = p.communicate()[0].strip().decode("utf-8")

            try:
                IP_addr = ipdb.interfaces[dev].ipaddr[0].get("address")
                netmask = ipdb.interfaces[dev].ipaddr[0].get("prefixlen")

                if output is "":
                    print("IP Settings: static")
                    print("Static IP: " + str(IP_addr))
                    if '24' in str(netmask):
                        print("Static Netmask: 255.255.255.0")
                else:
                    print("IP Settings: dhcp")
                    print("Static IP: " + str(IP_addr))
                    if '24' in str(netmask):
                        print("Static Netmask: 255.255.255.0")

            except (IndexError, KeyError):
                print("IP Settings: manual")
                print("Static IP: Null")
                print("Static Netmask: Null")
            
            gw = []

            for route_entry in ipdb.routes.tables[254].keys():
                if route_entry == "::1/128" or route_entry == "fe80::/64":
                    continue
        
                if ipdb.routes.tables[254][route_entry].oif == link_index:              
                    gw.append(ipdb.routes.tables[254][route_entry].get("gateway"))


            if gw == [None]:
                print("Static Gateway: 0.0.0.0")
            elif gw == []:
                print("Static Gateway: Null")
            else:
                print("Static Gateway: " + str(gw))



def main():
    iface_type()
    ip_settings()


if __name__ == "__main__":
    main()