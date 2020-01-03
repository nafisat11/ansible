import json
import argparse
import os

from iface_configs import *
from rajant_configs import *
from sysctl_configs import *
from wifi80211_configs import *
from ntp_configs import *
from mea_configs import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file", "-f", type=str, help="Enter the name of the json file", action="store"
    )
    args = parser.parse_args()

    filename = args.file
    json_directory = "/home/nafisa/ansible-playbooks/"
    if os.path.isfile(os.path.join(json_directory, filename)):
        json_filepath = os.path.realpath(os.path.join(json_directory, filename))
    else:
        print("Please enter valid filename")
        sys.exit(1)

    with open(json_filepath) as json_file:              #add checks to see if keys are present
        data_structure = json.load(json_file)
        interfaces_data = data_structure["data"].get("interfaces")
        rajant_data = data_structure["data"].get("rajant")
        sysctl_data = data_structure["data"].get("sysctl")
        wpa_supplicant_data = data_structure["data"]["80211"]["wpa_supplicant"]
        host_apd_data = data_structure["data"]["80211"]["host_apd"]
        crda_data = data_structure["data"]["80211"]["crda"]
        ntp_data = data_structure["data"].get("ntp")
        mea_data = data_structure["data"].get("mea")

        for iface in interfaces_data.keys():
            auto_prop(interfaces_data, iface).add_line()
            addrFam(interfaces_data, iface).add_line()

        for breadcrumb in rajant_data["breadcrumbs"]:
            RajantConfig(breadcrumb).write_config()

        for interface in wpa_supplicant_data:
            WpaSupplicantConfig(interface).write_config()

        for ap in host_apd_data:
            HostapdConfig(ap).write_config()

        for wireless_domain in crda_data:
            CrdaConfig(wireless_domain).write_config()

        for mea_device in mea_data:
            MeaConfig(mea_device).write_config()

        NtpConfig(ntp_data).write_config()

        SysctlConfig(sysctl_data).write_config()
