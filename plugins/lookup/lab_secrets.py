"""
Ansible secret lookup plugin for retrieving secrets from Vault.
"""

from __future__ import absolute_import, division, print_function

from typing import Any, Dict, List, Optional

from ansible.errors import AnsibleLookupError  # type: ignore
from ansible.plugins.lookup import LookupBase  # type: ignore
from ansible.utils.display import Display  # type: ignore
from home_lab_secrets import secret_actions

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

    def run(
        self, terms: List[str], variables: Optional[Dict[str, Any]] = None, **kwargs: Optional[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        self.set_options(var_options=variables, direct=kwargs)
        if len(terms) != 1:
            raise AnsibleLookupError("home_lab_secrets lookup expects a single argument")

        key: str = terms[0]

        try:
            data = secret_actions(key, "read", None)["secret"]
        except ValueError as e:
            raise AnsibleLookupError(f"Error retrieving secret: {e}") from e

        return [data]
