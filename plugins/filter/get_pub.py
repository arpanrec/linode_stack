"""
This module provides custom Ansible filter plugins to handle ECDSA key pairs.

Functions:
    get_encrypted_id_ecdsa_pub_key(id_ecdsa: str, password: str) -> str:
        Get the public key of an ECDSA key pair from an encrypted private key.

    get_unencrypted_id_ecdsa(id_ecdsa: str, password: str) -> str:
        Get the unencrypted private key of an ECDSA key pair.

Classes:
    FilterModule:
        Custom Ansible filter plugin to get the public key of an ECDSA key pair.

"""

from typing import Callable, Dict

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def get_encrypted_id_ecdsa_pub_key(id_ecdsa: str, password: str) -> str:
    """
    Get the public key of an ECDSA key pair
    """
    rsa_root_ca_key = serialization.load_ssh_private_key(
        data=id_ecdsa.encode("utf-8"),
        password=password.encode("utf-8"),
        backend=default_backend(),
    )
    rsa_root_ca_openssh_pub_key_bytes: bytes = rsa_root_ca_key.public_key().public_bytes(
        encoding=serialization.Encoding.OpenSSH, format=serialization.PublicFormat.OpenSSH
    )
    return rsa_root_ca_openssh_pub_key_bytes.decode("utf-8")


def get_unencrypted_id_ecdsa(id_ecdsa: str, password: str) -> str:
    """
    Get the unencrypted private key of an ECDSA key pair
    """
    rsa_root_ca_key = serialization.load_ssh_private_key(
        data=id_ecdsa.encode("utf-8"),
        password=password.encode("utf-8"),
        backend=default_backend(),
    )
    rsa_root_ca_openssh_no_pass_key_bytes: bytes = rsa_root_ca_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.OpenSSH,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return rsa_root_ca_openssh_no_pass_key_bytes.decode("utf-8")


# pylint: disable=too-few-public-methods
class FilterModule:
    """
    Custom Ansible filter plugin to get the public key of an ECDSA key pair
    """

    def filters(self) -> Dict[str, Callable[[str, str], str]]:
        """
        Return a dict mapping method names to method references
        """

        return {
            "get_encrypted_id_ecdsa_pub_key": get_encrypted_id_ecdsa_pub_key,
            "get_unencrypted_id_ecdsa": get_unencrypted_id_ecdsa,
        }
