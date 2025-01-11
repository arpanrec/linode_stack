"""
Ansible Module for managing Secret Squirrel secrets.
"""

# Copyright: (c) 2022, Arpan Mandal <arpan.rec@gmail.com>
# MIT (see LICENSE or https://en.wikipedia.org/wiki/MIT_License)
from __future__ import absolute_import, division, print_function

import os
import json
from typing import Any, Dict
from ansible.module_utils.basic import AnsibleModule  # type: ignore

# pylint: disable=C0103
__metaclass__ = type


DOCUMENTATION = r"""
---
module: home_lab_secrets

short_description: Ansible Module for managing Secret Squirrel secrets.

version_added: "1.0.0"

description: Ansible Module for managing Secret Squirrel secrets.

options:
    path:
        description: Rest Api endpoint
        required: false
        type: str
        default: "https://api.github.com"
    action:
        description: Action to be performed
        required: false
        type: str
        default: "get"
        choices:
            - get
            - update
            - delete
    value:
        description: Value of the secret
        required: false
        type: dict
author:
    - Arpan Mandal (mailto:arpan.rec@gmail.com)
"""

EXAMPLES = r"""
- name: Create or Update a repository secret
  home_lab_secrets:
      path: "/secret/project/key"
      action: "update"
      value: "my_secret_value"
"""

RETURN = r"""
secret:
    description: The secret value
    type: str | dict
"""


# pylint: disable=inconsistent-return-statements
def run_module() -> None:
    """
    Ansible main module
    """
    # define available arguments/parameters a user can pass to the module
    __secret_dir = "foo.secret"
    __data_file = "data.json"
    module_args = {
        "path": {"type": "str", "required": True},
        "action": {"type": "str", "required": False, "default": "get", "choices": ["get", "update", "delete"]},
        "value": {"required": False, "type": "dict"},
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)
    path = module.params["path"]
    action = module.params.get("action", "get")
    value = module.params.get("value", None)

    if action == "get":
        data_file_path = os.path.join(__secret_dir, path, __data_file)
        with open(data_file_path, "r", encoding="utf-8") as data_file:
            data: Dict[str, Any] = json.load(data_file)
        module.exit_json(changed=False, secret=data)
    elif action == "update":
        if value is None:
            module.fail_json(msg="Value is required for update action")
        data_file_dir = os.path.join(__secret_dir, path)
        if not os.path.exists(data_file_dir):
            os.makedirs(data_file_dir)
        data_file_path = os.path.join(data_file_dir, __data_file)
        with open(data_file_path, "w", encoding="utf-8") as data_file:
            json.dump(value, data_file, indent=4, sort_keys=True)
        module.exit_json(changed=True, secret=value)


def main() -> None:
    """
    Python Main Module
    """
    run_module()


if __name__ == "__main__":
    main()
