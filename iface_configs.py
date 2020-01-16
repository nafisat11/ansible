"""This module represents an interface stanza definition"""


class AddrOpts:
    """
    A class for processing ip address options.

    Attributes
    ----------
    address : str
        dotted quad ip address

    netmask : str
        netmask (dotted quad or number of bits)

    gateway : str
        default gateway address (dotted quad)
    """

    def __init__(self, data):
        """
        The constructor for the AddrOpts class.

        Parameters
        ----------
        data : dict
            dictionary containing interfaces option data specific to an address family
        """
        self.address = data.get("address", "")
        self.netmask = data.get("netmask", "")
        self.gateway = data.get("gateway", "")

    def stanza_line(self):
        """
        Returns string(s) formatted for an interface stanza
        """
        lines = ""
        if self.address != "":
            lines += "    {} {}\n".format("address", self.address)
        if self.netmask != "":
            lines += "    {} {}\n".format("netmask", self.netmask)
        if self.gateway != "":
            lines += "    {} {}\n".format("gateway", self.gateway)
        return lines


class IfaceOpts:
    """
    A class for processing generic interface command options.

    Attributes
    ----------
    pre_up : list
        command(s) to run before bringing interface up

    up : list 

    post_up : list
        command(s) to run after bringing interface up

    pre_down : list 
        command(s) to run before bringing interface down

    down : list 

    post_down : list 
        command(s) to run after bringing interface down
    """

    def __init__(self, data):
        """
        The constructor for the IfaceOpts class.

        Parameters
        ----------
        data : dict
            dictionary containing interfaces option data specific to an address family
        """
        self.pre_up = data.get("pre-up", [])
        self.up = data.get("up", [])
        self.post_up = data.get("post_up", [])
        self.pre_down = data.get("pre_down", [])
        self.down = data.get("down", [])
        self.post_down = data.get("post_down", [])

    def stanza_line(self):
        """
        Returns string(s) formatted for an interface stanza
        """
        lines = ""
        if self.pre_up:
            for opt in range(len(self.pre_up)):
                lines += "    {} {}\n".format("pre-up", self.pre_up[opt])
        if self.up:
            for opt in range(len(self.up)):
                lines += "    {} {}\n".format("up", self.up[opt])
        if self.post_up:
            for opt in range(len(self.post_up)):
                lines += "    {} {}\n".format("post-up", self.post_up[opt])
        if self.pre_down:
            for opt in range(len(self.pre_down)):
                lines += "    {} {}\n".format("post-up", self.pre_down[opt])
        if self.down:
            for opt in range(len(self.down)):
                lines += "    {} {}\n".format("post-up", self.down[opt])
        if self.post_down:
            for opt in range(len(self.post_down)):
                lines += "    {} {}\n".format("post-up", self.post_down[opt])
        return lines


class VlanOpts:
    """
    A class for processing vlan interface options.

    Attributes
    ----------
    vlan_parent : str
        physical link

    vlan_id : int
        vlan identifier
    """

    def __init__(self, data):
        """
        The constructor for the VlanOpts class

        Parameters
        ----------
        data : dict
            dictionary containing interfaces option data specific to an address family
        """
        self.vlan_parent = ""
        if data["vlan_opts"]:  # not empty
            if data["vlan_opts"].get("vlan-raw-device"):  # vlan-raw-device is not empty
                self.vlan_parent = data["vlan_opts"]["vlan-raw-device"].get(
                    "parent", ""
                )

    def stanza_line(self):
        """
        Returns string(s) formatted for an interface stanza wanting to setup a vlan
        """
        if self.vlan_parent != "":
            return "    vlan-raw-device {}\n".format(self.vlan_parent)
        else:
            return ""


class BridgeOpts:
    """
    A class for processing bridge interface options.

    Attributes
    ----------
    bridge_ports : list
        slave interfaces to add to bridge

    bridge_stp : str
        enable or disable spanning tree protocol

    bridge_maxwait : int
        max waiting time
    """

    def __init__(self, data):
        """
        The constructor for the BridgeOpts class

        Parameters
        ----------
        data : dict
            dictionary containing interfaces option data specific to an address family
        """
        self.bridge_ports = data["bridge_opts"].get("bridge_ports", [])
        self.bridge_stp = data["bridge_opts"].get("bridge_stp", "")
        self.bridge_maxwait = data["bridge_opts"].get("bridge_maxwait", "")

    def stanza_line(self):
        """
        Returns string(s) formatted for an interface stanza wanting to setup a bridge
        """
        lines = ""
        if self.bridge_ports:
            lines += "    {} {}\n".format("bridge_ports", " ".join(self.bridge_ports))
        if self.bridge_stp != "":
            lines += "    {} {}\n".format("bridge_stp", self.bridge_stp)
        if self.bridge_maxwait != "":
            lines += "    {} {}\n".format("bridge_maxwait", self.bridge_maxwait)
        else:
            return ""
        return lines


class WlanOpts:
    """
    A class for processing wlan interface options.

    Attributes
    ----------
    wpa_driver : str
        wlan driver

    wpa_roam : str
        enable roaming
    """

    def __init__(self, data):
        """
        The constructor for the WlanOpts class

        Parameters
        ----------
        data : dict
            dictionary containing interfaces option data specific to an address family
        """
        self.wpa_driver = data["wlan_opts"].get("wpa-driver", "")
        self.wpa_roam = data["wlan_opts"].get("wpa-roam", "")

    def stanza_line(self):
        """
        Returns string(s) formatted for an interface stanza wanting to setup a bridge
        """
        lines = ""
        if self.wpa_driver != "":
            lines += "    {} {}\n".format("wpa-driver", self.wpa_driver)

        if self.wpa_roam != "":
            lines += "    {} {}\n".format("wpa-roam", self.wpa_roam)
        else:
            return ""
        return lines


class MeaOpts:
    """
    A class for processing mea interface options.

    Attributes
    ----------
    post_up : list
        command(s) to run after bringing interface up
    """

    def __init__(self, data):
        """
        The constructor for the MeaOpts class

        Parameters
        ----------
        data : dict
            dictionary containing interfaces option data specific to an address family
        """
        self.post_up = data["mea_opts"].get("post-up", [])

    def stanza_line(self):
        """
        Returns string(s) formatted for an interface stanza wanting to setup a bridge
        """
        lines = ""
        if self.post_up:
            lines += "    {} {}\n".format("post-up", " ".join(self.post_up))
        else:
            return ""
        return lines


class IfaceDetails:
    """
    A class for manipulating interface stanza option data.

    Attributes
    ----------
    opts : list
        common options present within an interface stanza

    """

    def __init__(self, data):
        """
        The constructor for IfaceDetails class.

        Parameters
        ----------
        data : dict
            dictionary containing interfaces option data specific to an address family
        """
        self.opts = [
            AddrOpts(data),
            IfaceOpts(data),
            VlanOpts(data),
            BridgeOpts(data),
            WlanOpts(data),
            MeaOpts(data),
        ]

    def iface_stanza_details(self):
        """
        Returns a list containing strings formatted to represent an interface options' respective line(s)
        in an interface stanza
        """
        iface_stanza_details = []

        for opt in self.opts:
            iface_stanza_details.append(opt.stanza_line())

        return iface_stanza_details
