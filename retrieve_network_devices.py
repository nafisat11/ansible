import netifaces
import os
import subprocess
import glob


def slave_interfaces():
	cmd = '''sudo brctl show'''
	os.system(cmd)
	
	


def iface_type():
	#cmd = '''nmcli dev status | awk '{$3=$4=""; print $0}' | column -t'''
	#os.system(cmd)
	iface = os.listdir('/sys/class/net')
	for interface in iface:
		if interface != 'lo':
			print("\nInterface: " + interface)
			IP_cmd = '''ip addr show %s | grep "inet " | awk '{print $2}' | cut -d/ -f1'''%(interface)
			print("IP address: ")
			os.system(IP_cmd)
			iface_path = os.path.realpath(os.path.join('/sys/class/net', interface))


			for entry in os.listdir(iface_path):
				if entry == 'address':
					mac_addr_path = os.path.join(iface_path, entry)
					MAC_cmd = 'cat %s'%(mac_addr_path)
					print("MAC address: ")
					os.system(MAC_cmd)

				if entry == 'uevent':
					uevent_path = os.path.join(iface_path, entry)
					list_type = '''cat %s | grep "DEVTYPE"'''%(uevent_path)
					os.system(list_type)


			#if '/devices/virtual/net' in iface_path:
				#print("Type: virtual")
				#if 'bridge' in os.listdir(iface_path):
					#print("This is a bridge interface")

			
			#else:
				#print("Type: native")
				#if 'master' in os.listdir(iface_path):
					#print("This is a slave interface")
		


def parent_interfaces():
	p = subprocess.run(['sudo', 'cat', 'config'], cwd='/proc/net/vlan')
	
		

def main():
	iface_type()
	print("-"*80)
	slave_interfaces()
	print("-"*80)
	parent_interfaces()
	print("-"*80)

	#for interface in iface:
		#if interface != 'lo':
			#try:
				#for link in netifaces.ifaddresses(interface)[netifaces.AF_LINK]:
					#print("\nInterface: " + interface)
					#print("MAC Address: " + link['addr'])
			#except KeyError:
				#print("Null")

			#try:
				#for ip in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
					#print("IP address:", ip['addr'])
			#except KeyError:
				#print("IP address: Null")


if __name__ == '__main__':
	main()