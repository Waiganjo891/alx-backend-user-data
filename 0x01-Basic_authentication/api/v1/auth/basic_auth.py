#!/usr/bin/env python3
"""
BasicAuth module for the API authentication
"""
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    BasicAuth class for handling basic authentication
    """
    def extract_base64_authorization_header(
                                            self,
                                            authorization_header: str
                                            ) -> str:
        """
        Extracts the Base64 part of the Authorization
        header for a Basic Authentication.
        Returns:
            The Base64 part of the Authorization header if
            valid, otherwise None.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
                                           self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        Decodes a Base64 string and returns the decoded value
        as a UTF-8 string.
        Returns:
            The decoded value as a UTF-8 string if valid,
            otherwise None.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
                                 self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        Extracts user credentials from the decoded Base64 string.
        Returns:
            A tuple of the user email and password if valid,
            otherwise (None, None).
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
                                    self,
                                    user_email: str,
                                    user_pwd: str
                                    ) -> TypeVar('User'):
        """
        Returns the User instance based on his email and password.
        Args:
            user_email (str): The user's email address.
            user_pwd (str): The user's password.
        Returns:
            User: The User instance if credentials
            are valid, otherwise None.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = User.search({'email': user_email})
        if not users:
            return None
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request.
        Args:
            request: The request object.
        Returns:
            User: The User instance if authentication is successful,
            otherwise None.
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        base64_header = self.extract_base64_authorization_header(auth_header)
        if base64_header is None:
            return None
        decoded_header = self.decode_base64_authorization_header(base64_header)
        if decoded_header is None:
            return None
        email, password = self.extract_user_credentials(decoded_header)
        if email is None or password is None:
            return None
        user = self.user_object_from_credentials(email, password)
        return user
