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
        wpa_supplicant_data = data_structure["data"]["80211"]["wpa_supplicant"]
        host_apd_data = data_structure["data"]["80211"]["host_apd"]
        crda_data = data_structure["data"]["80211"]["crda"]
        ntp_data = data_structure["data"].get("ntp")
        mea_data = data_structure["data"].get("mea")

        for iface in interfaces_data.keys():
            with open("{}.conf".format(iface), "w") as iface_conf_file:
                if interfaces_data[iface]["auto"]:
                    iface_conf_file.write("auto {}\n".format(iface))

                if interfaces_data[iface]["addrFam"].get("inet"):
                    inet_family = ifaceDetails(
                        interfaces_data[iface]["addrFam"]["inet"]
                    )
                    iface_conf_file.write(
                        "iface {} inet {}\n".format(
                            iface, interfaces_data[iface]["addrFam"]["inet"]["mode"]
                        )
                    )
                    for detail in inet_family.details():
                        iface_conf_file.write(detail)

                if interfaces_data[iface]["addrFam"].get("inet6"):
                    inet6_family = ifaceDetails(
                        interfaces_data[iface]["addrFam"]["inet6"]
                    )
                    iface_conf_file.write(
                        "\niface {} inet6 {}\n".format(
                            iface, interfaces_data[iface]["addrFam"]["inet6"]["mode"]
                        )
                    )
                    for detail in inet6_family.details():
                        iface_conf_file.write(detail)
