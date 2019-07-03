from pyroute2 import IPRoute, IPDB 
import subprocess
from collections import Counter

ip = IPRoute()
ipdb = IPDB()

def ip_settings():
    iface = ipdb.by_name.keys()
    for dev in iface:
        kind = ipdb.interfaces[dev].get("kind")
        if kind == "vlan":
            
            print("\nInterfaces with VLAN Traffic: %s" %(dev))
            print("VLAN ID: " + str(ipdb.interfaces[dev].vlan_id))

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

            except (IndexError, KeyError):
                print("IP Settings: manual")
                print("Static IP: Null")
                print("Static Netmask: Null")
                print("Static Gateway: Null")

            link_index = ip.link_lookup(ifname=dev)[0]
            routes = []
            gw = []

            for route_entry in ipdb.routes.tables[254].keys():
                if route_entry == '::1/128' or route_entry == 'fe80::/64':
                    continue
        
                if ipdb.routes.tables[254][route_entry].oif == link_index:              
                    routes.append(ipdb.routes.tables[254][route_entry].oif)
                    gw.append(ipdb.routes.tables[254][route_entry].get('gateway'))

            print(gw)
            if routes.count(link_index) > 1:
                print("Additional routes")
                cmd = "netstat -rn | grep %s" %(dev)
                p = subprocess.Popen((cmd), shell=True, stdout=subprocess.PIPE)
                output = p.communicate()[0].strip().decode("utf-8")
                print(output)
            else:
                print("Additional routes: Null")

            #if len(gw) > 1:

                    

                    #gw = ipdb.routes.tables[254][route_entry].get('gateway')
                    #if gw:
                        #print("Static Gateway: " + str(gw))
                    #else:
                        #print("Static Gateway: 0.0.0.0")
            #routes = []
            #for i in ipdb.routes.tables[254]:
                #for key in ipdb.routes.tables[254][i]:
                    #value = ipdb.routes.tables[254][i][key]
                    #if key == 'oif':
                        #routes.append(value)
            #print(routes)


                    
def main():
    ip_settings()

if __name__ == "__main__":
    main()
