# -*- coding: utf-8 -*-
"""
Ansible Module for Search for the latest release in a GitHub repository.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type  # pylint: disable=invalid-name

import os
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
            - E(GET_HOMELAB_CREDS_USE_CACHE) environment variable can be used to set this option.
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

        use_cache: Optional[str] = self.get_option("use_cache")

        if use_cache:
            display.v(f"get_homelab_creds: Use cache set to {use_cache} in options.")

        if use_cache is None:
            display.v("get_homelab_creds: Use cache not set, using environment variable.")
            use_cache = os.getenv("GET_HOMELAB_CREDS_USE_CACHE", None)

        if (use_cache is not None) and ((type(use_cache) is bool and use_cache) or use_cache.lower() == "true"):
            display.warning("get_homelab_creds: Use cache set to True."
                            " This can expose sensitive information to other playbooks."
                            " Make sure to clear the cache after use.")
            return [_credential_manager.get_with_cache(terms[0])]

        display.v("get_homelab_creds: Not using cache.")
        return [_credential_manager.get(terms[0])]
