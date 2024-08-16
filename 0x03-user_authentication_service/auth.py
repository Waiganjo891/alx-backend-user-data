#!/usr/bin/env python3
"""
This module provides authentication-related utilities.
"""
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.
    Args:
        password (str): The password to be hashed.
    Returns:
        bytes: The salted hash of the input password.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


class Auth:
    """
    Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with email and password.
        Args:
            email (str): The user's email.
            password (str): The user's password.
        Returns:
            User: The newly created user object.
        Raises:
            ValueError: If a user with the provided
            email already exists.
        """
        existing_user = self._db.find_user_by(email=email)
        if existing_user:
            raise ValueError(f"User {email} already exists")
        hashed_password = _hash_password(password)
        new_user = self._db.add_user(
                                    email=email,
                                    hashed_password=hashed_password
                                    )
        return new_user


if __name__ == "__main__":
    print(_hash_password("Hello Holberton"))
