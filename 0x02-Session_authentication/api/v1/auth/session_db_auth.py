#!/usr/bin/env python3
"""
This module provides functionality for session
storage to database
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    This class provides functionality for session
    storage
    """
    def create_session(self, user_id=None):
        """
        Creates a new session for user

        Args:
            user_id (str): user id

        Returns:
            str: session id
        """
        if user_id is None:
            return None
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user = UserSession()
        user.user_id = user_id
        user.session_id = session_id
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns user id for session id

        Args:
            session_id (str): session id

        Returns:
            str: user id
        """
        user_id = super().user_id_for_session_id(session_id)
        return user_id

    def destroy_session(self, request=None):
        """
        Destroys session

        Args:
            request (obj): request object
        """
        is_destroyed = super().destroy_session(request)
        if is_destroyed:
            # Delete session from file
            session_id = request.cookies.get('session_id')
            user = UserSession.search({'session_id': session_id})
            if not user:
                return False
            user[0].remove()
            return True
