"""
Ansible secret lookup plugin for retrieving secrets from Vault.
"""

from __future__ import absolute_import, division, print_function

import json
import os
from typing import Any, Dict, List, Optional

from ansible.errors import AnsibleLookupError  # type: ignore
from ansible.plugins.lookup import LookupBase  # type: ignore
from ansible.utils.display import Display  # type: ignore

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

    __secret_dir = "foo.secret"
    __data_file = "data.json"

    def run(
        self, terms: List[str], variables: Optional[Dict[str, Any]] = None, **kwargs: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        self.set_options(var_options=variables, direct=kwargs)
        if len(terms) != 1:
            raise AnsibleLookupError("home_lab_secrets lookup expects a single argument")

        key: str = terms[0]

        if key.startswith("/"):
            raise AnsibleLookupError("Vault key should not start with /")
        if key.endswith("/"):
            raise AnsibleLookupError("Vault key should not end with /")
        if len(key) == 0:
            raise AnsibleLookupError("Vault key should not be empty")

        data_file_path = os.path.join(self.__secret_dir, key, self.__data_file)
        with open(data_file_path, "r", encoding="utf-8") as data_file:
            data: Dict[str, Any] = json.load(data_file)

        return [data]
