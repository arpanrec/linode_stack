# -*- coding: utf-8 -*-
"""
This module provides functions for initializing and interacting with HashiCorp Vault.
"""


class VaultOpsRetryError(ValueError):
    """
    Exception raised when the init_unseal process is to be tried.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)


class VaultOpsSafeExit(ValueError):
    """
    Exit the program safely.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)