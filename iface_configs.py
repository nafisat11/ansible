class IpAddress:
    def __init__(self, address):
        self._address = address

    @property
    def address(self):
        return self._address
    
    def stanza_line(self):
        if self._address != "":
            return "    {} {}\n".format("address", self._address)
        else:
            return ""

class IpNetmask:
    def __init__(self, netmask):
        self._netmask = netmask

    @property
    def netmask(self):
        return self._netmask
    
    def stanza_line(self):
        if self._netmask != "":
            return "    {} {}\n".format("netmask", self._netmask)
        else:
            return ""

class IpGateway:
    def __init__(self, gateway):
        self._gateway = gateway

    @property
    def gateway(self):
        return self._gateway
    
    def stanza_line(self):
        if self._gateway != "":
            return "    {} {}\n".format("gateway", self._gateway)
        else:
            return ""

class PreupOpt:
    def __init__(self, pre_up):
        self._pre_up = pre_up

    @property
    def pre_up(self):
        return self._pre_up
    
    def stanza_line(self):
        lines = ""
        if self._pre_up:
            for opt in range(len(self._pre_up)):
                lines += "    {} {}\n".format("pre-up", self._pre_up[opt])
            return lines
        else:
            return ""

class UpOpt:
    def __init__(self, up):
        self._up = up

    @property
    def up(self):
        return self._up
    
    def stanza_line(self):
        lines = ""
        if self._up:
            for opt in range(len(self._up)):
                lines += "    {} {}\n".format("up", self._up[opt])
            return lines
        else:
            return ""

class PostupOpt:
    def __init__(self, post_up):
        self._post_up = post_up

    @property
    def post_up(self):
        return self._post_up
    
    def stanza_line(self):
        lines = ""
        if self._post_up:
            for opt in range(len(self._post_up)):
                lines += "    {} {}\n".format("post-up", self._post_up[opt])
            return lines
        else:
            return ""

class PredownOpt:
    def __init__(self, pre_down):
        self._pre_down = pre_down

    @property
    def pre_down(self):
        return self._pre_down
    
    def stanza_line(self):
        lines = ""
        if self._pre_down:
            for opt in range(len(self._pre_down)):
                lines += "    {} {}\n".format("pre-down", self._pre_down[opt])
            return lines
        else:
            return ""

class DownOpt:
    def __init__(self, down):
        self._down = down

    @property
    def down(self):
        return self._down
    
    def stanza_line(self):
        lines = ""
        if self._down:
            for opt in range(len(self._down)):
                lines += "    {} {}\n".format("down", self._down[opt])
            return lines
        else:
            return ""

class PostdownOpt:
    def __init__(self, post_down):
        self._post_down = post_down

    @property
    def post_down(self):
        return self._post_down
    
    def stanza_line(self):
        lines = ""
        if self._post_down:
            for opt in range(len(self._post_down)):
                lines += "    {} {}\n".format("post-down", self._post_down[opt])
            return lines
        else:
            return ""

class VlanOpts:
    def __init__(self, vlan_opts):
        self._vlan_parent = vlan_opts.get("parent", "")
        self._vlan_id = vlan_opts.get("id", "")

    @property
    def vlan_parent(self):
        return self._vlan_parent

    @property
    def vlan_id(self):
        return self._vlan_id
    
    def stanza_line(self):
        if self._vlan_parent != "":
            return "    vlan-raw-device {}".format(self._vlan_parent)
        else:
            return ""

class BridgeOpts:
    def __init__(self, bridge_opts):
        self._bridge_ports = bridge_opts.get("bridge_ports", [])
        self._bridge_stp = bridge_opts.get("bridge_stp", "")
        self._bridge_maxwait = bridge_opts.get("bridge_maxwait", "")

    @property
    def bridge_ports(self):
        return self._bridge_ports

    @property
    def bridge_stp(self):
        return self._bridge_stp

    @property
    def bridge_maxwait(self):
        return self._bridge_maxwait
    
    def stanza_line(self):
        lines = ""
        if self._bridge_ports:
            lines += "    {} {}\n".format("bridge_ports", " ".join(self._bridge_ports))
        if self._bridge_stp != "":
            lines += "    {} {}\n".format("bridge_stp", self._bridge_stp)
        if self._bridge_maxwait != "":
            lines += "    {} {}\n".format("bridge_maxwait", self._bridge_maxwait)
        else:
            return ""
        return lines

class WlanOpts:
    def __init__(self, wlan_opts):
        self._wpa_driver = wlan_opts.get("wpa-driver", "")
        self._wpa_roam = wlan_opts.get("wpa-roam", "")

    @property
    def wpa_driver(self):
        return self._wpa_driver

    @property
    def wpa_roam(self):
        return self._wpa_roam

    def stanza_line(self):
        lines = ""
        if self._wpa_driver != "":
            lines += "    {} {}\n".format("wpa-driver", self._wpa_driver)

        if self._wpa_roam != "":
            lines += "    {} {}\n".format("wpa-roam", self._wpa_roam)
        else:
            return ""
        return lines

class MeaOpts:
    def __init__(self, mea_opts):
        self._post_up = mea_opts.get("post-up", [])

    @property
    def post_up(self):
        return self._post_up
    
    def stanza_line(self):
        lines = ""
        if self._post_up:
            lines += "    {} {}\n".format("post-up", " ".join(self._post_up))
        else:
            return ""
        return lines


class IfaceDetails:
    def __init__(self, data):
        self.address = IpAddress(data.get("address", ""))
        self.netmask = IpNetmask(data.get("netmask", ""))
        self.gateway = IpGateway(data.get("gateway", ""))
        self.pre_up = PreupOpt(data.get("pre-up", []))
        self.up = UpOpt(data.get("up", []))
        self.post_up = PostupOpt(data.get("post-up", []))
        self.pre_down = PredownOpt(data.get("pre-down", []))
        self.down = DownOpt(data.get("down", []))
        self.post_down = PostdownOpt(data.get("post-down", []))
        self.vlan_opts = VlanOpts(data.get("vlan_opts", {})) 
        self.bridge_opts = BridgeOpts(data.get("bridge_opts", {}))
        self.wlan_opts = WlanOpts(data.get("wlan_opts", {}))
        self.mea_opts = MeaOpts(data.get("mea_opts", {}))

    def iface_details(self):
        iface_stanza_details = []

        iface_stanza_details.append(self.address.stanza_line())
        iface_stanza_details.append(self.netmask.stanza_line())
        iface_stanza_details.append(self.gateway.stanza_line())
        iface_stanza_details.append(self.pre_up.stanza_line())
        iface_stanza_details.append(self.up.stanza_line())
        iface_stanza_details.append(self.post_up.stanza_line())
        iface_stanza_details.append(self.pre_down.stanza_line())
        iface_stanza_details.append(self.down.stanza_line())
        iface_stanza_details.append(self.post_down.stanza_line())
        iface_stanza_details.append(self.vlan_opts.stanza_line())
        iface_stanza_details.append(self.bridge_opts.stanza_line())
        iface_stanza_details.append(self.wlan_opts.stanza_line())
        iface_stanza_details.append(self.mea_opts.stanza_line())

        return iface_stanza_details
