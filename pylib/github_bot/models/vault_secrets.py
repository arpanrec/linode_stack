# *-* coding: utf-8 *-*
"""
This module defines data models for managing secrets and configurations related to GitHub, 
HashiCorp Vault, and other external services using Pydantic BaseModel.

Classes:
    GitHubProdDetails: Represents the GitHub production details.
    BotGpgDetails: Represents the GitHub Actions GPG key details.
    GitHubBotDetails: Represents the GitHub bot details.
    GithubDetails: Represents the GitHub details.
    RootPkiDetails: Represents the root PKI details.
    VaultAdminUserpassDetails: Represents the Vault admin userpass details.
    VaultSecrets: Represents the secrets required for interacting with HashiCorp Vault.

"""

from typing import Any, Dict, List, Union

from pydantic import BaseModel, Field


class GitHubProdDetails(BaseModel):
    """
    Represents the GitHub production details.
    """

    GH_PROD_API_TOKEN: str = Field(description="The GitHub bot API token.")


class BotGpgDetails(BaseModel):
    """
    Attributes:
        BOT_GPG_PRIVATE_KEY: str: The GitHub Actions GPG private key.
        BOT_GPG_PASSPHRASE: str: The GitHub Actions GPG passphrase.
    """

    BOT_GPG_PRIVATE_KEY: str = Field(description="The GitHub Actions GPG private key.")
    BOT_GPG_PASSPHRASE: str = Field(description="The GitHub Actions GPG passphrase.")


class GitHubBotDetails(BaseModel):
    """
    Represents the GitHub bot details.
    """

    GH_BOT_API_TOKEN: str = Field(description="The GitHub production API token.")


class GithubDetails(BaseModel):
    """
    Represents the GitHub details.
    """

    github_bot: GitHubBotDetails = Field(description="The GitHub bot details.")
    github_prod: GitHubProdDetails = Field(description="The GitHub production details.")
