from pyroute2 import IPRoute, IPDB 

ip = IPRoute()
ipdb = IPDB()

def ip_settings():
    iface = ipdb.by_name.keys()
    for dev in iface:
        kind = ipdb.interfaces[dev].get("kind")
        if kind == "vlan":
            print("Interfaces with VLAN Traffic: %s" %(dev))
            print("VLAN ID: -1")

            IP_addr = ipdb.interfaces[dev].ipaddr.ipv4

            try:
                print("IP Settings: Static")
                print("Static IP: " + str(IP_addr[0].get("address")))
                if '24' in str(IP_addr[0].get("prefixlen")):
                    print("Static Netmask: 255.255.255.0")
            except (IndexError, KeyError):
                print("IP Settings: Manual")
                print("Static IP: Null")
                print("Static Netmask: Null")

            for route_entry in ipdb.routes.tables[254].keys():
                if route_entry == '::1/128' or route_entry == 'fe80::/64':
                    continue

                gateway = ipdb.routes.tables[254][route_entry].get('gateway')
                multi_routes = ipdb.routes.tables[254][route_entry].get('multipath')

                if gateway is None:
                    print("Static Gateway: 0.0.0.0")
                else:
                    print("Static Gateway: " + str(gateway))

                #if str(IP_addr[0].get('address')).split('.')[:3] == route_entry.split('.')[:3]:
                    #if len(multi_routes) == 0:
                        #print("Additional Routes: Null")


                    
def main():
    ip_settings()

if __name__ == "__main__":
    main()