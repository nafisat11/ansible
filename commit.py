#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Nafisa Tabassum <nafisatabassum@3d-p.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
module: commit

short_description: Commit staged changes

version_added: "2.8"

description:
    - This module will commit staged changes
    - Files and directories listed in a removal manifest are removed
    - Commands to disable services and flush firewall rules are executed
    - Templates are moved in place to respective subdirectories in /etc

options:
    files:
        description:
            - Files containing staged changes
        type: dict
        required: true
        aliases: [ filenames, names ]
    source:
        description:
            - Temporary working directory path
        type: path
        required: true
        aliases: [ workdir_path ]
    dest:
       description:
            - Directory to move files into place
       type: path
       required: true
       aliases: [ destdir_path ]

extends_documentation_fragment:
    - files

author:
    - Nafisa Tabassum (nafisatabassum@3d-p.com)
"""

EXAMPLES = """
# Commit staged network changes
- commit:
    files: {"removal_manifest": "/tmp/staged_changesuu9yr3.root/.remove",
            "command_execution": "/tmp/staged_changesuu9yr3.root/.execute"}
    source: "/tmp/staged_changesuu9yr3.root/etc/"
    dest: "/etc/"
"""

RETURN = """
"""

import os
import shutil
import subprocess
from ansible.module_utils.basic import AnsibleModule

src_to_dest = {}


def main():
    module = AnsibleModule(
        argument_spec=dict(
            files=dict(type="dict", required=True, aliases=["filenames", "names"]),
            source=dict(type="path", required=True, aliases=["workdir_path"]),
            dest=dict(type="path", required=True, aliases=["destdir_path"]),
        ),
        supports_check_mode=True,
    )
    files = module.params["files"]
    source = module.params["source"]
    dest = module.params["dest"]
    removal_manifest_failures = []
    command_execution_failures = []
    move_in_place_failures = []

    with open(files["removal_manifest"]) as removal_manifest:
        for entry in removal_manifest:
            entry = entry.strip()
            if os.path.exists(entry):
                try:
                    os.remove(entry)
                except OSError as err:
                    removal_manifest_failures.append(
                        "{} could not be removed: {}".format(entry, err)
                    )

    with open(files["command_execution"]) as command_execution:
        for command in command_execution:
            command = command.strip().split(" ")
            try:
                run_command = subprocess.Popen(
                    command,
                    close_fds=True,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except (OSError, IOError) as err:
                failed_command = " ".join(command)
                command_execution_failures.append(
                    "Command {} could not run: {}".format(failed_command, err)
                )

    for dirpath, dirs, files in os.walk(source):
        for filename in files:
            new_src_path = os.path.join(dirpath, filename)
            new_dest = source.split(dest)[0]
            new_dest_path = os.path.dirname(new_src_path).split(new_dest)[-1]
            src_to_dest[new_src_path] = new_dest_path

    for src, dst in src_to_dest.items():
        if os.path.exists(dst) and os.path.exists(src):
            try:
                shutil.move(src, dst)
            except (OSError, IOError, shutil.Error) as err:
                move_in_place_failures.append(
                    "Moving {} to {} failed: {}".format(src, dst, err)
                )

    module.exit_json(
        changed=True,
        removal_manifest_failures=removal_manifest_failures,
        move_in_place_failures=move_in_place_failures,
        command_execution_failures=command_execution_failures,
    )


if __name__ == "__main__":
    main()
