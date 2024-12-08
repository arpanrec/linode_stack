# *- encoding: utf-8 -*
"""
This module defines the VaultServer model using Pydantic for data validation and parsing.

Classes:
    VaultServer: Represents the details of a Vault server, including its cluster and API addresses,
                 Vault nodes, Ansible options, host keys, and additional Ansible inventory groups.

"""
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from .vault_node import VaultNode


class VaultServer(BaseModel):
    """
    Represents the details of a Vault server.

    Attributes:
        is_vault_server (bool): Whether the server is a Vault server.
        cluster_addr_fqdn (str, optional): The fully qualified domain name of the cluster address.
        cluster_ip (str, optional): The IP address of the cluster.
        api_addr_fqdn (str, optional): The fully qualified domain name of the API address.
        api_ip (str, optional): The IP address of the API.
        vault_nodes (Dict[str, VaultNode]): A dictionary of Vault server node details.
        ansible_opts (Dict[str, str], optional): Additional Ansible options for the Vault server.
        host_keys (List[str], optional): A list of host keys for the Vault server.
        root_ca_key_pem_as_ansible_priv_ssh_key (bool): Whether to use the root CA key as an Ansible private SSH key.
        ansible_inventory_extra_groups (List[str], optional): A list of extra groups to add to the Ansible inventory.
    """

    is_vault_server: bool = Field(default=True)
    cluster_addr_fqdn: Optional[str] = Field(default=None)
    cluster_ip: Optional[str] = Field(default=None)
    api_addr_fqdn: Optional[str] = Field(default=None)
    api_ip: Optional[str] = Field(default=None)
    vault_nodes: Dict[str, VaultNode] = Field(default={})
    ansible_opts: Dict[str, str] = Field(default={})
    host_keys: List[str] = Field(default=[])
    root_ca_key_pem_as_ansible_priv_ssh_key: bool = Field(default=True)
    ansible_inventory_extra_groups: List[str] = Field(default=[])
