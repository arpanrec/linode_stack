# *-* coding: utf-8 *-*
"""
This module provides functionality to set up GitHub access for both bot and user repositories
using Vault for secret management.

Functions:
    setup_github(vault_ha_client: VaultHaClient) -> None:
        Sets up GitHub access for the bot and users by adding vault access to GitHub user repositories
        and adding a GPG key to the bot GitHub account.

Modules:
    github:
        Contains functions to add vault access to GitHub user repositories.
    github_bot:
        Contains functions to add GPG keys to the bot GitHub account.
    models.ha_client:
        Contains the VaultHaClient class used for interacting with Vault.

"""

import logging

from ..models.ha_client import VaultHaClient
from .github import add_vault_access_to_github
from .github_bot import add_gpg_to_bot_github

LOGGER = logging.getLogger(__name__)


def setup_github(vault_ha_client: VaultHaClient) -> None:
    """
    Setup GitHub access for the bot and users.
    """

    LOGGER.info("Adding vault access to GitHub user repositories")
    add_vault_access_to_github(vault_ha_client=vault_ha_client)

    LOGGER.info("Add gpg key to bot GitHub account")
    add_gpg_to_bot_github(vault_ha_client=vault_ha_client)
