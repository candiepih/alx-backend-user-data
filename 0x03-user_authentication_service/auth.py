#!/usr/bin/env python3
"""
This module contains the methods and attributes needed
for the authentication
"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
import uuid
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import Union


def _hash_password(password: str) -> bytes:
    """
    Method that encrypts a provided password.

    Args:
        password: The password to be encrypted.

    Returns:
        bytes: The encrypted password.
    """
    return hashpw(password.encode(), gensalt())


def _generate_uuid() -> str:
    """
    Method that generates a UUID.

    Returns:
        str: The generated UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.

    Attributes:
        _db: The database object.
    """

    def __init__(self):
        """
        Constructor for the Auth class.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Method that registers a user in the database.

        Args:
            email: The email of the user.
            password: The password of the user.

        Raises:
            ValueError: If the user already exists.

        Returns:
            User: The user object.
        """
        try:
            users_found = self._db.find_user_by(email=email)
            if users_found:
                raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password).decode('utf-8')
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Method that validates a login.

        Args:
            email: The email of the user.
            password: The password of the user.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        if not email or not password:
            return False
        try:
            users_found = self._db.find_user_by(email=email)
            hashed_password = users_found.hashed_password
            return checkpw(password.encode(),
                           hashed_password.encode('utf-8'))
        except (NoResultFound, InvalidRequestError):
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """
        Method that creates a session for a user.

        Args:
            email: The email of the user.

        Returns:
            str: The session id.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except (NoResultFound, ValueError):
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Method that gets a user from a session id.

        Args:
            session_id: The session id.

        Returns:
            User: The user object.
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Method that destroys a session for a user.

        Args:
            user_id: The user id.
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Method that gets a reset password token.

        Args:
            email: The email of the user.

        Raises:
            ValueError: If the user does not exist.

        Returns:
            str: The reset password token.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user.reset_token:
                return user.reset_token
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Method that updates the password of a user.

        Args:
            reset_token: The reset password token.
            password: The new password.

        Returns:
            bool: True if the password was updated, False otherwise.

        Raises:
            ValueError: If the reset token is invalid.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password).decode('utf-8')
            self._db.update_user(user.id, hashed_password=hashed_password,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
