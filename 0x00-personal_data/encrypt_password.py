#!/usr/bin/env python3
"""
"""
from typing import ByteString
from bcrypt import hashpw, gensalt, checkpw


def hash_password(password: str) -> ByteString:
    """
    A function that hashes a password using bcrypt.

    Args:
        password: The password to be hashed.

    Returns:
        ByteString: The hashed password.
    """
    salt = hashpw(password.encode(), gensalt())
    return salt


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates that the provided password matches
    the hashed password.

    Args:
        hashed_password: The hashed password to be validated.
        password: The password to be validated.

    Returns:
        bool: True if the password matches the hashed password,
            False otherwise.
    """
    return checkpw(password.encode(), hashed_password)