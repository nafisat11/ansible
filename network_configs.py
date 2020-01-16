# creates interfaces file(s)
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

    with open(json_filepath) as json_file:  # add checks to see if keys are present
        data_structure = json.load(json_file)
        interfaces_data = data_structure["data"].get("interfaces")
        rajant_data = data_structure["data"].get("rajant")
        sysctl_data = data_structure["data"].get("sysctl")
        wifi80211_data = data_structure["data"]["80211"]
        ntp_data = data_structure["data"].get("ntp")
        mea_data = data_structure["data"].get("mea")

        for iface in interfaces_data.keys():
            with open("{}.conf".format(iface), "w") as iface_conf_file:
                if interfaces_data[iface]["auto"]:
                    iface_conf_file.write("auto {}\n".format(iface))

                if interfaces_data[iface]["addrFam"].get("inet"):
                    inet_stanza = IfaceDetails(
                        interfaces_data[iface]["addrFam"]["inet"]
                    )
                    iface_conf_file.write(
                        "iface {} inet {}\n".format(
                            iface, interfaces_data[iface]["addrFam"]["inet"]["mode"]
                        )
                    )
                    for detail in inet_stanza.iface_stanza_details():
                        iface_conf_file.write(detail)

                if interfaces_data[iface]["addrFam"].get("inet6"):
                    inet6_stanza = IfaceDetails(
                        interfaces_data[iface]["addrFam"]["inet6"]
                    )
                    iface_conf_file.write(
                        "\niface {} inet6 {}\n".format(
                            iface, interfaces_data[iface]["addrFam"]["inet6"]["mode"]
                        )
                    )
                    for detail in inet6_stanza.iface_stanza_details():
                        iface_conf_file.write(detail)

        for device, data in rajant_data.items():
            if device == "breadcrumbs":
                for bc_data in data:
                    with open("{}".format(bc_data["serial"]), "w") as bc_conf_file:
                        bc_conf_file.write(RajantConfig(bc_data).device_settings())

        for config, data in wifi80211_data.items():
            if config == "wpa_supplicant":
                for supplicant_data in data:
                    with open(
                        "wpa_supplicant.{}.conf".format(supplicant_data["interface"]),
                        "w",
                    ) as wpa_supplicant_file:
                        print(WpaSupplicantConfig(supplicant_data).network_props[0].key_mgmt)
            
            if config == "host_apd":
                for host_apd_data in data:
                    with open(
                        "host_apd.{}.conf".format(host_apd_data["interface"]), "w"
                    ) as host_apd_file:
                        pass
            
            if config == "crda":
                for crda_data in data:
                    print(crda_data)
                    with open(
                        "crda_{}".format(crda_data["REGDOMAIN"]), "w"
                    ) as crda_file:
                        crda_file.write(
                            "{}={}".format("REGDOMAIN", crda_data.get("REGDOMAIN", ""))
                        )
