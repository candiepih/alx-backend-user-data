#!/usr/bin/env python3
"""
User Session
"""
from models.base import Base


class UserSession(Base):
    """
    Storing user session data

    Attributes:
        user_id (str): User ID
        session_id (str): Session ID
    """
    def __init__(self, *args: list, **kwargs: dict):
        """
        Initializes UserSession class

        Args:
            args: User ID and Session ID
            kwargs: dictionary of arguments
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
