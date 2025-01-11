"""
"""

from __future__ import absolute_import, division, print_function

import json
from typing import Any, Dict, List, Optional, Union

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

    __secret_file = "foo.secret.json"

    def run(
        self, terms: List[str], variables: Optional[Dict[str, Any]] = None, **kwargs: Optional[Dict[str, Any]]
    ) -> Union[List[str], List[Dict[str, Any]]]:
        self.set_options(var_options=variables, direct=kwargs)
        if len(terms) != 1:
            raise AnsibleLookupError("vaultops_secrets lookup expects a single argument")

        term: str = terms[0]

        with open(self.__secret_file, "r", encoding="utf-8") as f:
            all_secrets: Dict[str, Any] = json.load(f)

        path = term.split("/")

        for key in path:
            all_secrets = all_secrets[key]
        return [all_secrets]
