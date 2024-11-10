# -*- coding: utf-8 -*-
"""
Ansible Module for Search for the latest release in a GitHub repository.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type  # pylint: disable=invalid-name

from typing import Any, Dict, List, Optional

from ansible.errors import AnsibleLookupError  # type: ignore
from ansible.plugins.lookup import LookupBase  # type: ignore
from homelab.get_cred import Bitwarden  # type: ignore

DOCUMENTATION = """
---
    name: get_homelab_creds
    author:
        - Arpan Mandal <me@arpanrec.com>
    short_description: Get Credentials for Homelab.
    description:
        - This lookup plugin retrieves the credentials for the Homelab.
        - For bitwarden path should be like <Organization Name>/<Collection Name>/<Item Name>/<Field Name>.
    options:
        _terms:
            description: Path for the credentials.
            required: true
            type: str
        get_homelab_creds_is_file:
            description: If the path is a file.
            required: false
            type: bool
            default: false
        get_homelab_creds_use_cache:
            description:
                - Use cache for credentials.
            required: false
            type: bool
            default: true
"""

_creds_manager = Bitwarden()


class LookupModule(LookupBase):
    """
    Lookup module that retrieves version details.
    """

    def _var(self, var_value):
        return self._templar.template(var_value, fail_on_undefined=True)

    def run(self, terms: List[str], variables: Optional[Dict[str, Any]] = None, **kwargs: Dict[str, Any]) -> List[str]:
        """
        Run the lookup module.
        """

        self.set_options(var_options=variables, direct=kwargs)

        if not terms:
            raise AnsibleLookupError("No terms provided for lookup")

        if len(terms) > 1:
            raise AnsibleLookupError(f"Only one term is allowed for lookup, got {len(terms)}, {terms}")

        if variables is not None:
            self._templar.available_variables = variables
        variables_ = getattr(self._templar, "_available_variables", {})

        is_file = self.get_option("is_file", True)
        use_cache = self.get_option("use_cache")
        if use_cache:
            return [_creds_manager.get_with_cache(terms[0], is_file)]

        return [_creds_manager.get(terms[0], is_file)]  # type: ignore
