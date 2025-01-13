"""
This module provides functionality to manage secrets in a specified directory.
It supports reading, writing, and deleting secrets stored in JSON files.

Functions:
    secret_actions(key: str, action: str, value: Any) -> Dict[str, Any]:
        Executes the specified action (read, write, delete) on the secret identified by the key.

Environment Variables:
    HOME_LAB_SECRETS_DIR: The directory where secrets are stored. Defaults to ${HOME}/home-lab.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


def secret_actions(key: str, action: str, value: Any) -> Dict[str, Any]:
    """
    Executes the specified action (read, write, delete) on the secret identified by the key.

    Args:
        key: Key of the secret. Must not start or end with / and cannot be empty.
        action: Action to be performed (read, write, delete).
        value: Value of the secret.

    Returns:
        A dictionary containing the following

    """
    # define available arguments/parameters a user can pass to the module
    __data_dir = os.environ.get("HOME_LAB_SECRETS_DIR", None)

    if __data_dir is None:
        __data_dir = os.path.join(Path.home(), "home-lab")

    __data_file = "data.json"

    if key is None or action is None:
        raise ValueError("Key and action are required")

    if action not in ["read", "write", "delete"]:
        raise ValueError("Invalid action, must be one of read, write, delete")

    if key.startswith("/"):
        raise ValueError("Key cannot start with /")
    if key.endswith("/"):
        raise ValueError("Key cannot end with /")
    if key == "":
        raise ValueError("Key cannot be empty")

    match action:
        case "read":
            if value is not None:
                raise ValueError("Value is not required for get action")
            data_file_path = os.path.join(__data_dir, key, __data_file)
            with open(data_file_path, "r", encoding="utf-8") as data_file:
                data: Dict[str, Any] = json.load(data_file)
            return {"changed": False, "secret": data}
        case "write":
            if value is None:
                raise ValueError("Value is required for update action")
            data_file_dir = os.path.join(__data_dir, key)
            if not os.path.exists(data_file_dir):
                os.makedirs(data_file_dir)
            data_file_path = os.path.join(data_file_dir, __data_file)

            if os.path.exists(data_file_path):
                now = datetime.now()
                backup_file = os.path.join(data_file_dir, f"{now.strftime('%Y%m%d%H%M%S')}_{__data_file}")
                os.rename(data_file_path, backup_file)

            with open(data_file_path, "w", encoding="utf-8") as data_file:
                json.dump(value, data_file, indent=4, sort_keys=True)
            return {"changed": True, "secret": value}
        case "delete":
            if value is not None:
                raise ValueError("Value is not required for delete action")
            data_file_dir = os.path.join(__data_dir, key)
            if os.path.exists(data_file_dir):
                os.remove(data_file_dir)
            return {"changed": True, "secret": {}}
        case _:
            raise ValueError("Invalid action, must be one of read, write, delete")
