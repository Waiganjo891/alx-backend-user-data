#!/usr/bin/env python3
"""
Auth module
"""
from flask import request
from typing import List, TypeVar


User = TypeVar('User')


class Auth:
    """
    Auth class to manage API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method to determine if authentication is required
        Args:
            path (str): The path to be checked
            excluded_paths (List[str]): A list of paths that
            do not require authentication
        Returns:
            bool: True if authentication is required, False otherwise
        """
        if path is None:
            return True
        if not excluded_paths:
            return True
        if not path.endswith('/'):
            path += '/'
        for excluded_path in excluded_paths:
            if excluded_path.endswith('/') and path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Method to retrieve the authorization
        header from the request
        Args:
            request: The Flask request object
        Returns:
            str: None as a placeholder
        """
        return None

    def current_user(self, request=None) -> User:
        """
        Method to retrieve the current user from the request
        Args:
            request: The Flask request object
        Returns:
            User: None as a placeholder
        """
        return None
