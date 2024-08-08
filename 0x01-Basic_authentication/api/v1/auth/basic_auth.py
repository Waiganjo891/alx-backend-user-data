#!/usr/bin/env python3
"""
BasicAuth module for the API authentication
"""
import base64
from api.v1.auth.auth import Auth


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
