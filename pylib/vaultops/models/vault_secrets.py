# *-* coding: utf-8 *-*
"""
This module defines data models for managing secrets and configurations related to GitHub, 
HashiCorp Vault, and other external services using Pydantic BaseModel.

Classes:
    GitHubProdDetails: Represents the GitHub production details.
    BotGpgDetails: Represents the GitHub Actions GPG key details.
    GitHubBotDetails: Represents the GitHub bot details.
    GithubDetails: Represents the GitHub details.
    RootPkiDetails: Represents the root PKI details.
    VaultAdminUserpassDetails: Represents the Vault admin userpass details.
    VaultSecrets: Represents the secrets required for interacting with HashiCorp Vault.

"""

from typing import Any, Dict, List, Union

from pydantic import BaseModel, Field


class RootPkiDetails(BaseModel):
    """
    Represents the root PKI details.
    """

    root_ca_key_password: str = Field(description="The password for the root CA key.")
    root_ca_key_pem: str = Field(description="The PEM-encoded root CA key.")
    root_ca_cert_pem: str = Field(description="The PEM-encoded root CA certificate.")


class VaultAdminUserpassDetails(BaseModel):
    """
    Represents the Vault admin userpass details.
    """

    vault_admin_user: str = Field(description="The username of the Vault admin user.")
    vault_admin_password: str = Field(description="The password of the Vault admin user.")
    vault_admin_userpass_mount_path: str = Field(description="The mount path for the Vault admin userpass.")
    vault_admin_policy_name: str = Field(description="The name of the Vault admin policy.")
    vault_admin_client_cert_p12_passphrase: str = Field(
        description="The passphrase for the Vault admin client certificate."
    )


class VaultSecrets(BaseModel):
    """
    Represents the secrets required for interacting with HashiCorp Vault.
    """

    vault_ha_hostname: str = Field(description="The hostname of the Vault HA cluster.")
    vault_ha_port: int = Field(description="The port number of the Vault HA cluster.")
    root_pki_details: RootPkiDetails = Field(description="The root PKI details.")
    vault_admin_userpass_details: VaultAdminUserpassDetails = Field(description="The Vault admin userpass details.")
    external_services: Dict[str, Union[str, bool, int, Dict[str, Any], List[Any]]] = Field(
        default={}, description="The external services required for the Vault HA cluster."
    )
    ansible_inventory: Dict[str, Union[str, bool, int, Dict[str, Any], List[Any]]] = Field(
        default={}, description="The Ansible inventory details."
    )
