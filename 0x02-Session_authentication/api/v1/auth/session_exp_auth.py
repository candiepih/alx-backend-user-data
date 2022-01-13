#!/usr/bin/env python3
"""
Contains the SessionExpAuth class that implements
the session expiration authentication method.
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    Implements the session expiration authentication method.

    Attributes:
        session_duration (int): The duration
        of the session in seconds.
    """

    def __init__(self):
        """
        Initializes the SessionExpAuth class.
        """
        duration = getenv("SESSION_DURATION")
        if not duration or not duration.isnumeric():
            self.session_duration = 0
        else:
            self.session_duration = int(duration)

    def create_session(self, user_id=None):
        """
        Creates a new session.

        Args:
            user_id (int): The user id.

        Returns:
            dict: The session.
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        super().user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the user id for the given session id.

        Args:
            session_id (str): The session id.

        Returns:
            int: The user id.
        """
        if not session_id:
            return None
        session_dictionary = super()\
            .user_id_by_session_id.get(session_id)
        if not session_dictionary:
            return None
        if self.session_duration <= 0:
            return session_dictionary.get('user_id')
        created_at = session_dictionary.get('created_at')
        if not created_at:
            return None
        if created_at + timedelta(seconds=self.session_duration) < \
                datetime.now():
            super().user_id_by_session_id.pop(session_id, None)
            return None
        return session_dictionary.get('user_id')
