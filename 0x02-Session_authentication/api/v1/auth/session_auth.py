#!/usr/bin/env python3
"""
Contains class SessionAuth that handles
session authentication.
"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """
    Handles session authentication.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session.

        Args:
            user_id: The user id.

        Returns:
            The session id.
        """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns the user id for the session id.

        Args:
            session_id: The session id.

        Returns:
            The user id.
        """
        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieves user based on cookie value

        Args:
            request: The request object.

        Returns:
            The user object.
        """
        user_cookie = self.session_cookie(request)
        if user_cookie is None:
            return None
        user_id = self.user_id_for_session_id(user_cookie)
        if isinstance(user_id, dict):
            user_id = user_id.get('user_id')
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Destroys the session.

        Args:
            request: The request object.
        """
        if not request:
            return False
        user_cookie = self.session_cookie(request)
        if user_cookie is None:
            return False
        user_id = self.user_id_for_session_id(user_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[user_cookie]
        return True
