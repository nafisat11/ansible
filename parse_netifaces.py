import debinterface

def main():
    netiface = {}
    iface = []
    interfaces = debinterface.Interfaces(interfaces_path="interfaces")
    adapters = interfaces.adapters

    for ad in adapters:
        netiface.setdefault(ad.attributes["name"], [])

    print(netiface)

    





if __name__ == '__main__':
    main()
