# -*- coding: utf-8 -*-
"""
Ansible lookup plugin to get secrets
"""

from __future__ import absolute_import, division, print_function

import os
import subprocess  # nosec B404
from typing import Any, Dict, List, Optional

# pylint: disable=invalid-name
__metaclass__ = type


from ansible.plugins.lookup import LookupBase  # type: ignore


def __bw_exec(
    cmd: List[str], ret_encoding: str = "UTF-8", env_vars: Optional[Dict[str, str]] = None, is_raw: bool = True
) -> str:
    """
    Executes a Bitwarden CLI command and returns the output as a string.
    """
    cmd = ["bw"] + cmd

    if is_raw:
        cmd.append("--raw")

    cli_env_vars = os.environ

    if env_vars is not None:
        cli_env_vars.update(env_vars)
    command_out = subprocess.run(
        cmd, capture_output=True, check=False, encoding=ret_encoding, env=cli_env_vars, timeout=10
    )  # nosec B603
    # if len(command_out.stderr) > 0:
    # LOGGER.warning("Error executing command %s", command_out.stderr)
    command_out.check_returncode()
    return command_out.stdout


class LookupModule(LookupBase):
    """
    Ansible lookup plugin to get secrets
    """

    def run(
        self, terms: Optional[List[str]], variables: Optional[Dict[str, Any]] = None, **kwargs: Optional[Dict[str, Any]]
    ) -> List[str]:
        """
        get secrets
        """
        if not terms:
            raise LookupError("No terms provided")

        if len(terms) != 1:
            raise LookupError("Only one term is allowed")

        self.set_options(var_options=variables, direct=kwargs)

        field: Optional[str] = None
        collection_id: Optional[str] = None
        organization_id: Optional[str] = None
        search: str = "name"
        attachment_name: Optional[str] = None
        attachment_id: Optional[str] = None
        item = terms[0]

        if kwargs:
            search = str(kwargs.get("search", "name"))

            if "collection_id" in kwargs:
                collection_id = str(kwargs.get("collection_id"))

            if "organization_id" in kwargs:
                organization_id = str(kwargs.get("organization_id"))

            if "field" in kwargs:
                field = str(kwargs.get("field"))

            if "attachment_name" in kwargs:
                attachment_name = str(kwargs.get("attachment_name"))

            if "attachment_id" in kwargs:
                attachment_id = str(kwargs.get("attachment_id"))

        if search not in ["name", "id"]:
            raise LookupError("Invalid search field, only 'name' or 'id' is allowed")

        if (attachment_name or attachment_id) and field:
            raise LookupError("Only one of 'field' or 'attachment_name' or 'attachment_id' is allowed")

        return [terms[0]]
