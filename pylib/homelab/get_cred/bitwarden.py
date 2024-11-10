import json
import os
import subprocess
import tempfile
from typing import Dict, List, Optional

try:
    from cachier import cachier
except ImportError as e:
    raise ImportError("Please install cachier using `pip install cachier`") from e
except Exception as e:
    raise ValueError("Unknown error occurred while importing cachier") from e


class Bitwarden:  # pylint: disable=too-few-public-methods
    """
    A class for interacting with the Bitwarden CLI.
    """

    _status: Optional[str] = None

    @staticmethod
    def __bw_exec(cmd: List[str], ret_encoding: str = "UTF-8", env_vars: Optional[Dict[str, str]] = None) -> str:
        """
        Execute the Bitwarden CLI command.
        """
        cmd = ["bw"] + cmd + ["--raw"]
        cli_env_vars = os.environ
        if env_vars:
            cli_env_vars.update(env_vars)
        command_out = subprocess.run(
            cmd, capture_output=True, check=False, encoding=ret_encoding, env=cli_env_vars, timeout=10, shell=False
        )
        command_out.check_returncode()
        if len(command_out.stdout) > 0:
            return command_out.stdout

        if len(command_out.stderr) > 0:
            return command_out.stderr
        return ""

    def __get_organization_id(self, organization_name: str) -> str:
        organization_id = ""
        organizations = json.loads(self.__bw_exec(["list", "organizations"]))
        for organization in organizations:
            if organization["name"] == organization_name:
                if organization_id != "":
                    raise ValueError(f"Multiple organizations found with the name {organization_name}")
                organization_id = organization["id"]
        if organization_id == "":
            raise ValueError(f"No organization found with the name {organization_name}")
        return organization_id

    def __get_collection_id(self, collection_name: str, organization_id: str) -> str:
        collection_id = ""
        collections = json.loads(self.__bw_exec(["list", "org-collections", "--organizationid", organization_id]))
        for collection in collections:
            if collection["name"] == collection_name:
                if collection_id != "":
                    raise ValueError(f"Multiple collections found with the name {collection_name}")
                collection_id = collection["id"]
        if collection_id == "":
            raise ValueError(f"No collection found with the name {collection_name}")
        return collection_id

    def __get_item_id(self, item_name: str, collection_id: str) -> str:
        item_id = ""
        items = json.loads(self.__bw_exec(["list", "items", "--collectionid", collection_id]))
        for item in items:
            if item["name"] == item_name:
                if item_id != "":
                    raise ValueError(f"Multiple items found with the name {item_name}")
                item_id = item["id"]
        if item_id == "":
            raise ValueError(f"No item found with the name {item_name}")
        return item_id

    @staticmethod
    def __get_field(fields: List[Dict[str, str]], field_name: str) -> str:
        field_value = ""
        for field in fields:
            if field["name"] == field_name:
                if field_value != "":
                    raise ValueError(f"Multiple fields found with the name {field_name}")
                field_value = field["value"]
        if field_value == "":
            raise ValueError(f"No field found with the name {field_name}")
        return field_value

    @staticmethod
    def __get_attachment_id(attachments: List[Dict[str, str]], file_name: str) -> str:
        attachment_id = ""
        for attachment in attachments:
            if attachment["fileName"] == file_name:
                if attachment_id != "":
                    raise ValueError(f"Multiple attachments found with the name {file_name}")
                attachment_id = attachment["id"]
        if attachment_id == "":
            raise ValueError(f"No attachment found with the name {file_name}")
        return attachment_id

    @cachier()
    def get_with_cache(self, path: str, is_file: bool = False) -> str:
        """
        Get the secret from Bitwarden with caching.
        """

        return self.get(path, is_file)

    def clear_cache(self) -> None:
        """
        Clear the cache.
        """
        self.get_with_cache.clear_cache()

    # pylint: disable=too-many-locals
    def get(self, path: str, is_file: bool = False) -> str:
        """
        Get the secret from Bitwarden without caching.
        """
        if len(path) == 0:
            raise ValueError("Path cannot be empty.")

        if path.endswith("/"):
            raise ValueError("Path cannot end with a slash.")

        if not self._status:
            self._status = json.loads(self.__bw_exec(["status"]))["status"]

        if self._status != "unlocked":
            raise ValueError("Bitwarden is not unlocked.")

        organization_name = path.split("/")[0]
        organization_id = self.__get_organization_id(organization_name)
        collection_name = "/".join(path.split("/")[1:-2])
        collection_id = self.__get_collection_id(collection_name, organization_id)

        item_name = path.split("/")[-2:-1][0]
        item_id = self.__get_item_id(item_name, collection_id)

        item = json.loads(self.__bw_exec(["get", "item", item_id]))
        fields = item["fields"]
        field_name = path.split("/")[-1]
        if is_file:
            attachments = item["attachments"]
            attachment_id = self.__get_attachment_id(attachments, field_name)
            attachment_file = tempfile.NamedTemporaryFile(delete=False)  # pylint: disable=consider-using-with
            attachment_content = self.__bw_exec(["get", "attachment", attachment_id, "--itemid", item_id])
            attachment_file.write(attachment_content.encode())
            attachment_file.close()
            return attachment_file.name

        field_value = self.__get_field(fields, field_name)
        return field_value
