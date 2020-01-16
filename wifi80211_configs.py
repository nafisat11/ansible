class GlobalProps:
    def __init__(self, data):
        self.interface = data.get("interface", "")
        self.autoscan = data.get("autoscan", "")
        self.roaming_thresholds = data.get("roaming_thresholds", "")
        self.roaming_threshold_ceiling = data.get("roaming_threshold_ceiling", "")
        self.signal_threshold = data.get("signal_threshold", "")
        self.interval_below_threshold = data.get("interval_below_threshold", "")
        self.interval_above_threshold = data.get("interval_above_threshold", "")

    def global_lines(self):
        lines = ""
        if self.interface:
            lines += "{}={}\n\n".format("interface", self.interface)
        if self.autoscan:
            lines += "{}={}\n\n".format("autoscan", self.autoscan)
        if self.roaming_thresholds:
            lines += "{}={}\n\n".format("roaming_thresholds", self.roaming_thresholds)
        if self.roaming_threshold_ceiling:
            lines += "{}={}\n\n".format("roaming_threshold_ceiling", self.roaming_threshold_ceiling)
        if self.signal_threshold:
            lines += "{}={}\n\n".format("signal_threshold", self.signal_threshold)
        if self.interval_below_threshold:
            lines += "{}={}\n\n".format("interval_below_threshold", self.interval_below_threshold)
        if self.interval_above_threshold:
            lines += "{}={}\n\n".format("interval_above_threshold", self.interval_above_threshold)
        return lines

class NetworkProps:
    def __init__(self, data): #overwrites if there are multiple network stanzas
        self.key_mgmt = data.get("key_mgmt", "")
        self.scan_ssid = data.get("scan_ssid", "")
        self.ssid = data.get("ssid", "")
        self.id_str = data.get("id_str", "")
        self.proto = data.get("proto", "")
        self.psk_hash = data.get("psk_hash", "")
        self.psk_text = data.get("psk_text", "")
        self.bgscan = data.get("bgscan", "")
        self.auth_alg = data.get("auth_alg", "")

    def network_stanza_lines(self):
        lines = ""
        lines += "network={\n"
        if self.key_mgmt:
            lines += "    {}={}\n".format("key_mgmt", self.key_mgmt)
        if self.scan_ssid:
            lines += "    {}={}\n".format("scan_ssid", self.scan_ssid)
        if self.ssid:
            lines += "    {}={}\n".format("ssid", self.ssid)
        if self.id_str:
            lines += "    {}={}\n".format("id_str", self.id_str)
        if self.proto:
            lines += "    {}={}\n".format("proto", self.proto)
        if self.psk_hash:
            lines += "    {}={}\n".format("psk_hash", self.psk_hash)
        if self.psk_text:
            lines += "    {}={}\n".format("psk_text", self.psk_text)
        if self.bgscan:
            lines += "    {}={}\n".format("bgscan", self.bgscan)
        if self.auth_alg:
            lines += "    {}={}\n".format("auth_alg", self.auth_alg)
        lines += "}\n\n"
        return lines

class WpaSupplicantConfig:                 
    def __init__(self, data): 
        self.global_props = GlobalProps(data)
        self.network_props = [NetworkProps(data) for data in data["networks"]]
        
    def config(self):
        for props in self.props:
            for net_props


class HostapdConfig:             
    def __init__(self, data):      
        self.ctrl_interface = data.get("ctrl_interface", "")
        self.bridge = data.get("bridge", "")
        self.interface = data.get("interface", "")
        self.driver = data.get("driver", "")
        self.ssid = data.get("ssid", "")
        self.hw_mode = data.get("hw_mode", "")
        self.channel = data.get("channel", "")
        self.macaddr_acl = data.get("macaddr_acl", "")
        self.auth_algs = data.get("auth_algs", "")
        self.ignore_broadcast_ssid = data.get("ignore_broadcast_ssid", "")
        self.wme_enabled = data.get("wme_enabled", "")
        self.ieee80211n = data.get("ieee80211n", "")
        self.ht_capab = data.get("ht_capab", "")
        self.wpa = data.get("wpa", "")
        self.wpa_passphrase = data.get("wpa_passphrase", "")
        self.wpa_key_mgmt = data.get("wpa_key_mgmt", "")
        self.wpa_pairwise = data.get("wpa_pairwise", "")
        self.rsn_pairwise = data.get("rsn_pairwise", "")
        self.wep_default_key = data.get("wep_default_key", "")
        self.wep_key0 = data.get("wep_key0", "")
