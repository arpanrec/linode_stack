# -*- coding: utf-8 -*-
"""
Ansible Module for Search for the latest release in a GitHub repository.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type  # pylint: disable=invalid-name

from typing import Any, Dict, List, Optional

from ansible.errors import AnsibleLookupError  # type: ignore
from ansible.plugins.lookup import LookupBase  # type: ignore
from ansible.utils.display import Display  # type: ignore
from homelab.get_cred import Bitwarden  # type: ignore

DOCUMENTATION = """
---
    name: get_homelab_creds
    author:
        - Arpan Mandal <me@arpanrec.com>
    short_description: Get Credentials for Homelab.
    description:
        - This lookup plugin retrieves the credentials for the Homelab.
    options:
        _terms:
            description: Path for the credentials.
            required: true
            type: str
        is_file:
            description: If the path is a file.
            required: false
            type: bool
            default: false
"""

_creds_manager = Bitwarden()


def run_module() -> None:
    """
    Search for the latest release in a GitHub repository.
    """


display = Display()


class LookupModule(LookupBase):
    """
    Lookup module that retrieves version details.
    """

    def run(self, terms: List[str], variables: Optional[Dict[str, Any]] = None, **kwargs: Dict[str, Any]) -> List[str]:
        """
        Run the lookup module.
        """

        self.set_options(var_options=variables, direct=kwargs)

        if not terms:
            raise AnsibleLookupError("No terms provided for lookup")

        if len(terms) > 1:
            raise AnsibleLookupError(f"Only one term is allowed for lookup, got {len(terms)}, {terms}")

        is_file = self.get_option("is_file", False)

        return [_creds_manager.get(terms[0], is_file)]  # type: ignore
