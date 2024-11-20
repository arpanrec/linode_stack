# -*- coding: utf-8 -*-
"""
Ansible lookup plugin to get secrets
"""

from __future__ import absolute_import, division, print_function

import datetime
import json
import os
import subprocess  # nosec B404
from typing import Any, Dict, List, Optional

from ansible.errors import AnsibleLookupError  # type: ignore
from ansible.plugins.lookup import LookupBase  # type: ignore
from ansible.utils.display import Display  # type: ignore

try:
    from cachier import cachier
except ImportError as e:
    raise AnsibleLookupError("Please install cachier with 'pip install cachier'") from e

display = Display()
# pylint: disable=invalid-name
__metaclass__ = type


class LookupModule(LookupBase):
    """
    Ansible lookup plugin to get secrets
    """

    __item: str
    __ret: Optional[str] = None
    __search: str = "name"
    __cache_location: Optional[str] = None

    def __get_custom_field(self, field_name: str) -> str:
        item_dict = json.loads(self.__bw_exec(["get", "item", self.__item]))
        fields: List[Dict[str, Any]] = item_dict["fields"]
        value: Optional[str] = None
        for field in fields:
            if field["name"] == field_name:
                if value is not None:
                    raise AnsibleLookupError("Multiple fields with the same name found")
                value = field.get("value", None)
                if not value or len(value) == 0:
                    raise AnsibleLookupError("Field has no value")

        if not value:
            raise AnsibleLookupError("Field not found")

        return value

    def __get_attachment(self, attachment_name: Optional[str], attachment_id: Optional[str]) -> str:
        item_dict: Optional[Dict[str, Any]] = None
        item_id: str
        if self.__search == "name":
            item_dict = dict(json.loads(self.__bw_exec(["get", "item", self.__item])))
            item_id = str(item_dict.get("id"))
        elif self.__search == "id":
            item_id = self.__item
        else:
            raise AnsibleLookupError("Invalid search type, only 'name' or 'id' is allowed")

        if not attachment_id:
            if not item_dict:
                item_dict = dict(json.loads(self.__bw_exec(["get", "item", item_id])))
            if not attachment_id and attachment_name:
                if "attachments" not in item_dict:
                    raise AnsibleLookupError("No attachments found")
                attachments: List[Dict[str, Any]] = item_dict["attachments"]
                for att in attachments:
                    if attachment_name and att["fileName"] == attachment_name:
                        if attachment_id is not None:
                            raise AnsibleLookupError("Multiple attachments with the same name found")
                        attachment_id = att["id"]

        if not attachment_id:
            raise AnsibleLookupError("Attachment not found")

        attachment_str = self.__bw_exec(["get", "attachment", attachment_id, "--itemid", item_id])
        return attachment_str

    @cachier(stale_after=datetime.timedelta(minutes=5), cache_dir=__cache_location)
    def __bw_exec_with_cache(
        self,
        cmd: List[str],
        ret_encoding: str = "UTF-8",
        env_vars: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        Executes a Bitwarden CLI command and returns the output as a string.
        """
        return self.__bw_exec_subprocess(cmd, ret_encoding, env_vars)

    def __bw_exec_without_cache(
        self,
        cmd: List[str],
        ret_encoding: str = "UTF-8",
        env_vars: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        Executes a Bitwarden CLI command and returns the output as a string.
        """
        return self.__bw_exec_subprocess(cmd, ret_encoding, env_vars)

    @staticmethod
    def __bw_exec_subprocess(
        cmd: List[str],
        ret_encoding: str = "UTF-8",
        env_vars: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        Executes a Bitwarden CLI command and returns the output as a string.
        """
        cmd = ["bw"] + cmd

        cmd.append("--raw")

        cli_env_vars = os.environ

        if env_vars is not None:
            cli_env_vars.update(env_vars)

        display.vvv(f"Executing Bitwarden CLI command: {' '.join(cmd)}")
        command_out = subprocess.run(
            cmd, capture_output=True, check=False, encoding=ret_encoding, env=cli_env_vars, timeout=10
        )  # nosec B603
        if command_out.returncode != 0:
            raise AnsibleLookupError(
                "Bitwarden CLI command failed, error: " f"{command_out.stderr if len(command_out.stderr) > 0 else None}"
            )
        return command_out.stdout

    def __bw_exec(
        self,
        cmd: List[str],
        ret_encoding: str = "UTF-8",
        env_vars: Optional[Dict[str, str]] = None,
    ) -> str:

        if self.__cache_location:
            return self.__bw_exec_with_cache(cmd, ret_encoding, env_vars)
        return self.__bw_exec_without_cache(cmd, ret_encoding, env_vars)

    # pylint: disable=too-many-branches
    def run(
        self, terms: Optional[List[str]], variables: Optional[Dict[str, Any]] = None, **kwargs: Optional[Dict[str, Any]]
    ) -> List[str]:
        """
        get secrets
        """
        if not terms:
            raise AnsibleLookupError("No terms provided")

        if len(terms) != 1:
            raise AnsibleLookupError("Only one term is allowed")

        self.set_options(var_options=variables, direct=kwargs)

        self.__item = terms[0]
        field: Optional[str] = None
        attachment_name: Optional[str] = None
        attachment_id: Optional[str] = None

        if variables and len(variables) > 1 and "secrets_lookup_cache_location" in variables:
            self.__cache_location = str(variables["secrets_lookup_cache_location"])

        if kwargs:

            if "field" in kwargs:
                field = str(kwargs["field"])

            if "attachment_name" in kwargs:
                attachment_name = str(kwargs["attachment_name"])

            if "attachment_id" in kwargs:
                attachment_id = str(kwargs["attachment_id"])

            if "search" in kwargs:
                self.__search = str(kwargs["search"])

            if "secrets_lookup_cache_location" in kwargs:
                self.__cache_location = str(kwargs["secrets_lookup_cache_location"])

        if self.__search not in ["name", "id"]:
            raise AnsibleLookupError("Invalid search type, only 'name' or 'id' is allowed")

        if (attachment_name or attachment_id) and field:
            raise AnsibleLookupError("Only one of 'field' or ('attachment_name' or 'attachment_id') is allowed")

        if attachment_name and attachment_id:
            raise AnsibleLookupError("Only one of 'attachment_name' or 'attachment_id' is allowed")

        if not attachment_name and not attachment_id and not field:
            raise AnsibleLookupError("One of 'field' or 'attachment_name' or 'attachment_id' is required")

        if field in ["username", "password", "totp", "uri", "notes"]:
            self.__ret = self.__bw_exec(["get", field, self.__item])
        elif field:
            self.__ret = self.__get_custom_field(field)
        elif attachment_name or attachment_id:
            self.__ret = self.__get_attachment(attachment_name, attachment_id)
        else:
            raise AnsibleLookupError("Invalid field")

        if not self.__ret or len(self.__ret) == 0:
            raise AnsibleLookupError("No available fields found")

        # display.vvvvvv(f"Secrets: {self.__ret}, type: {type(self.__ret)}")

        return [str(self.__ret)]
