from augeas import Augeas
import debinterface

def main():
    aug = Augeas(root="/")
    matches = aug.match("/files/etc/network/interfaces/*")
    for entry in matches:
        print(aug.get(entry))

def test():
    interfaces = debinterface.Interfaces(interfaces_path="interfaces")
    adapters = interfaces.adapters
    print("Static:")
    for ad in adapters:
        if ad.attributes["source"] == "static":
            ip = ad.attributes["address"]
            print(ad.attributes["name"], ip)

    print("DHCP:")
    for ad in adapters:
        if ad.attributes["source"] == "dhcp":
            print(ad.attributes["name"])





if __name__ == '__main__':
    #main()
    test()