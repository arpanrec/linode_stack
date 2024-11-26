"""
This module provides a custom Ansible lookup plugin named `vaultops_secrets`.

The `vaultops_secrets` lookup plugin is used to retrieve secrets from a specified source.
It expects a single argument and returns the provided argument as a list.

Classes:
    LookupModule: The main class that implements the lookup functionality.

Exceptions:
    AnsibleError: Raised when the lookup plugin encounters an error.
    AnsibleParserError: Raised when there is a parsing error in the Ansible playbook.

Functions:
    run(terms: List[str], variables: Optional[Dict[str, Any]] = None, **kwargs: Optional[Dict[str, Any]]) -> List[str]:
        Executes the lookup plugin with the provided terms and variables.

"""

from __future__ import absolute_import, division, print_function
import json
from typing import Any, Dict, List, Optional

from ansible.errors import AnsibleError  # type: ignore
from ansible.plugins.lookup import LookupBase  # type: ignore
from ansible.utils.display import Display  # type: ignore
import hvac  # type: ignore
from vaultops.models.ha_client import VaultHaClient

__metaclass__ = type
display = Display()


class LookupModule(LookupBase):
    """
    LookupModule is a custom Ansible lookup plugin for retrieving secrets from Vault.
    Methods:
        run(
            terms: List[str], variables: Optional[Dict[str, Any]] = None, **kwargs: Optional[Dict[str, Any]]
        ) -> List[str]:
            Executes the lookup plugin with the provided terms and variables.
    Raises:
        AnsibleError: If the number of terms provided is not exactly one.
    Returns:
        List[str]: A list containing the single term provided.
    """

    def run(
        self, terms: List[str], variables: Optional[Dict[str, Any]] = None, **kwargs: Optional[Dict[str, Any]]
    ) -> List[str]:
        if len(terms) != 1:
            raise AnsibleError("vaultops_secrets lookup expects a single argument")

        if not variables or len(variables) == 0 or "vault_ha_client" not in variables:
            raise AnsibleError("No variables provided vault_ha_client")

        term: str = terms[0]
        term_split = term.split("/")

        mount_path = term_split[0]
        secret_json_key = term_split[-1]
        secret_path = "/".join(term_split[1:-1])

        display.v(f"mount_path: {mount_path}")
        display.v(f"secret_path: {secret_path}")
        display.v(f"secret_json_key: {secret_json_key}")

        vault_ha_client: VaultHaClient = VaultHaClient.model_validate(variables["vault_ha_client"])
        client: hvac.Client = vault_ha_client.hvac_client()

        secret_version_response = client.secrets.kv.v2.read_secret_version(mount_point=mount_path, path=secret_path)

        print(secret_version_response)

        return [""]
