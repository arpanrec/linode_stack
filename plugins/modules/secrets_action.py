"""
Ansible Module for managing secrets.
"""

# Copyright: (c) 2022, Arpan Mandal <arpan.rec@gmail.com>
# MIT (see LICENSE or https://en.wikipedia.org/wiki/MIT_License)
from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule  # type: ignore
from home_lab_secrets import secret_actions

# pylint: disable=C0103
__metaclass__ = type


DOCUMENTATION = r"""
---
module: secrets_action

short_description: ""

version_added: "1.0.0"

description: ""

options:
    key:
        description: Key of the secret. Must not start or end with / and cannot be empty.
        required: true
        type: str
    action:
        description: Action to be performed
        required: false
        type: str
        default: "read"
        choices:
            - read
            - write
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
  secrets_action:
      key: "/secret/project/key"
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
    module_args = {
        "key": {"type": "str", "required": True},
        "action": {"type": "str", "required": False, "default": "get", "choices": ["read", "write", "delete"]},
        "value": {"required": False, "type": "dict"},
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)
    key = module.params["key"]
    action = module.params.get("action", "get")
    value = module.params.get("value", None)

    try:
        data = secret_actions(key, action, value)
        module.exit_json(changed=data["changed"], secret=data["secret"])
    except ValueError as e:
        module.fail_json(msg=f"Error retrieving secret: {e}", changed=False)


def main() -> None:
    """
    Python Main Module
    """
    run_module()


if __name__ == "__main__":
    main()
