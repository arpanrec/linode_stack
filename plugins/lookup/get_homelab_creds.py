# -*- coding: utf-8 -*-
"""
Ansible Module for Search for the latest release in a GitHub repository.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type  # pylint: disable=invalid-name

from typing import Any, Dict, List, Optional

from ansible.errors import AnsibleLookupError  # type: ignore
from ansible.plugins.lookup import LookupBase  # type: ignore
from ansible.utils.display import Display # type: ignore

from homelab.get_cred import Bitwarden  # type: ignore

DOCUMENTATION = """
---
name: get_homelab_creds
author:
    - Arpan Mandal <me@arpanrec.com>
short_description: Get Credentials for Homelab.
description:
    - This lookup plugin retrieves the credentials for the Homelab.
    - For bitwarden path should be like <Organization Name>/<Collection Name>/<Item Name>/<Field Name or Attachment
      Name>.
options:
    _terms:
        description: Path for the credentials.
        required: true
        type: str
    use_cache:
        description:
            - Use cache for credentials.
            - `get_homelab_creds_use_cache` variable can be used to set this option.
        required: false
"""

_credential_manager = Bitwarden()

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

        use_cache = self.get_option("use_cache")
        if not use_cache and variables:
            use_cache = str(variables.get("get_homelab_creds_use_cache"))

        use_cache_bool = use_cache.lower() == "true" if use_cache else False

        if use_cache_bool:
            return [_credential_manager.get_with_cache(terms[0])]

        return [_credential_manager.get(terms[0])]
