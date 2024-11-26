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

import datetime
from typing import Any, Dict, List, Optional

import hvac  # type: ignore
from ansible.errors import AnsibleLookupError  # type: ignore
from ansible.plugins.lookup import LookupBase  # type: ignore
from ansible.utils.display import Display  # type: ignore
from hvac.exceptions import InvalidPath  # type: ignore
from vaultops.models.ha_client import VaultHaClient

try:
    from cachier import cachier
except ImportError as e:
    raise AnsibleLookupError("Please install cachier with 'pip install cachier'") from e

__metaclass__ = type  # pylint: disable=invalid-name
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

    __variable_options: Optional[Dict[str, Any]] = None

    def run(
        self, terms: List[str], variables: Optional[Dict[str, Any]] = None, **kwargs: Optional[Dict[str, Any]]
    ) -> List[str]:
        self.set_options(var_options=variables, direct=kwargs)
        self.__variable_options = variables
        if len(terms) != 1:
            raise AnsibleLookupError("vaultops_secrets lookup expects a single argument")

        if not variables or len(variables) == 0 or "vault_ha_client" not in variables:
            raise AnsibleLookupError("No variables provided vault_ha_client")

        term: str = terms[0]
        display.warning(
            f"Using cache location: '{self.__lookup_token.cache_dpath()}',"
            " Make sure to remove the directory after execution.\n"
        )
        return self.__lookup_token(term)

    @cachier(stale_after=datetime.timedelta(minutes=60))
    def __lookup_token(self, term: str) -> List[str]:
        if not self.__variable_options or len(self.__variable_options) == 0:
            raise AnsibleLookupError("No variables provided")

        term_split = term.split("/")

        mount_path = term_split[0]
        json_key = term_split[-1]
        item_path = "/".join(term_split[1:-1])

        if (  # pylint: disable=too-many-boolean-expressions
            not mount_path or not item_path or not json_key or mount_path == "" or item_path == "" or json_key == ""
        ):
            raise AnsibleLookupError(f"Invalid secret path format: {term}")

        display.v(f"mount_path: {mount_path}")
        display.v(f"secret_path: {item_path}")
        display.v(f"secret_json_key: {json_key}")

        vault_ha_client: VaultHaClient = VaultHaClient.model_validate(self.__variable_options["vault_ha_client"])
        client: hvac.Client = vault_ha_client.hvac_client()

        try:
            secret_version_response = client.secrets.kv.v2.read_secret_version(mount_point=mount_path, path=item_path)
            if json_key not in secret_version_response["data"]["data"]:
                raise AnsibleLookupError(f"Secret key {json_key} not found in Vault")
            return [secret_version_response["data"]["data"][json_key]]
        except InvalidPath as ex:
            raise AnsibleLookupError(f"Secret path {item_path} not found in Vault") from ex
