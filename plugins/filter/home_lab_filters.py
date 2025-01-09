"""
This is a custom Ansible filter plugin that provides a filter to get a list of partitions
 UUIDs from the ansible_devices dictionary.
"""

# Make coding more python3-ish, this is required for contributions to Ansible
from __future__ import absolute_import, division, print_function

import base64
import hashlib
import os
from typing import Any, Dict, List, Union

# pylint: disable=C0103,invalid-name
__metaclass__ = type

# not only visible to ansible-doc, it also 'declares' the options the plugin requires and how to configure them.
DOCUMENTATION = """
"""


def generate_qbittorrent_hash(password: str) -> str:
    """
    Generate a PBKDF2 hash for a password.
    """

    # Generate a random salt
    salt = os.urandom(16)
    iterations = 100000  # Number of iterations
    algorithm = "sha512"  # Hashing algorithm

    # Generate PBKDF2 hash
    dk = hashlib.pbkdf2_hmac(algorithm, password.encode(), salt, iterations)

    # Base64 encode the salt and hash
    encoded_salt = base64.b64encode(salt).decode()
    encoded_hash = base64.b64encode(dk).decode()

    # Format for qBittorrent
    qbittorrent_hash = f"@ByteArray({encoded_salt}:{encoded_hash})"

    return qbittorrent_hash


def get_part_uuids_from_ansible_devices(
    ansible_devices: Dict[str, Dict[str, Dict[str, Dict[str, Union[Any, str]]]]]
) -> List[str]:
    """
    Get a list of partitions UUIDs from the ansible_devices dictionary.
    """
    all_uuids: List[str] = []
    for device in ansible_devices:
        if "partitions" not in ansible_devices[device] or len(ansible_devices[device]["partitions"]) < 1:
            continue
        partitions = ansible_devices[device]["partitions"]

        for partition in partitions.values():
            if "uuid" in partition:
                all_uuids.append(partition["uuid"])
    return all_uuids


# pylint: disable=too-few-public-methods
class FilterModule:
    """
    Home Lab all ansible filters.
    """

    def filters(self) -> dict[str, object]:
        """
        Returns a dictionary mapping filter names to filter functions.

        This function is used by Ansible to discover all of the filters in this plugin.
        The returned dictionary maps the name of each filter (as a string) to the function that implements the filter.

        Returns:
            dict: A dictionary where the keys are filter names and the values are the corresponding filter functions.
        """
        return {
            "get_part_uuids_from_ansible_devices": get_part_uuids_from_ansible_devices,
            "generate_qbittorrent_hash": generate_qbittorrent_hash,
        }
