#!/usr/bin/env python3
"""Defines the auth model"""

from typing import Union
from user import Base, User
import bcrypt
from db import DB
from uuid import uuid4


def _hash_password(password: str) -> str:
    """takes in a password string arguments and returns bytes
    """
    if password is None:
        return None
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password


def _generate_uuid() -> str:
    """The function should return a string
    representation of a new UUID.
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ takes mandatory email and password
        string arguments and return a User object.
        """
        if email is None or password is None:
            return None

        user = None
        try:
            user = self._db.find_user_by(email=email)
            if isinstance(user, User):
                raise ValueError(f'User {email} already exists.')
        except Exception as e:
            if isinstance(e, ValueError):
                raise e
            else:
                hashedPwd = _hash_password(password)
                user = self._db.add_user(email, hashedPwd)
                return user

    def valid_login(self, email: str, password: str) -> bool:
        """  It expects email and password as
            arguments and return a boolean if password is valid
        """
        if email is None or password is None:
            return False
        try:
            user = self._db.find_user_by(email=email)
            if isinstance(user, User):
                hashed_password = user.hashed_password
                if bcrypt.checkpw(password.encode(), hashed_password):
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            return False

    def create_session(self, email: str) -> str:
        """ takes an email string argument and returns
        the session ID as a string.
        """
        if email is None or not isinstance(email, str):
            return None
        try:
            user = self._db.find_user_by(email=email)
            if isinstance(user, User):
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
        except Exception as e:
            return None

    def get_user_from_session_id(self, id_session: str) -> User:
        """ It takes a single session_id string argument
                and returns the corresponding User or None.
        """
        if id_session is None or not isinstance(id_session, str):
            return None
        try:
            user = self._db.find_user_by(session_id=id_session)
            if not isinstance(user, User):
                return None
            return user
        except Exception as e:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Get reset password token.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Update the password using reset token and new password.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_pwd = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_pwd)
            self._db.update_user(user.id, reset_token=None)
        except NoResultFound:
            raise ValueError
        return None

    def destroy_session(self, user_id: int) -> None:
        """The method takes a single user_id integer
        argument and returns None.
        """
        if user_id is None or not isinstance(user_id, int):
            return None
        return self._db.update_user(user_id, session_id=None)
