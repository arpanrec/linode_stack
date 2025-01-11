"""
Ansible Module for managing Secret Squirrel secrets.
"""

# Copyright: (c) 2022, Arpan Mandal <arpan.rec@gmail.com>
# MIT (see LICENSE or https://en.wikipedia.org/wiki/MIT_License)
from __future__ import absolute_import, division, print_function

import json
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
        type: str | dict
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
    __secret_file = "foo.secret.json"
    module_args = {
        "path": {"type": "str", "required": True},
        "action": {"type": "str", "required": False, "default": "get", "choices": ["get", "update", "delete"]},
        "value": {"required": False},
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)
    path = module.params["path"]
    action = module.params.get("action", "get")
    value = module.params.get("value", None)

    all_secrets = {}
    with open(__secret_file, "r", encoding="utf-8") as f:
        all_secrets = json.load(f)

    path_list = path.split("/")
    if action == "get":
        for key in path_list:
            all_secrets = all_secrets.get(key, {})
        module.exit_json(changed=False, secret=all_secrets)
    elif action == "update":
        if value is None:
            module.fail_json(msg="Value is required for update action")
        for key in path_list[:-1]:
            all_secrets = all_secrets[key]
        all_secrets[path_list[-1]] = value
        with open(__secret_file, "w", encoding="utf-8") as f:
            json.dump(all_secrets, f, indent=4)
        module.exit_json(changed=True, secret=all_secrets)


def main() -> None:
    """
    Python Main Module
    """
    run_module()


if __name__ == "__main__":
    main()
