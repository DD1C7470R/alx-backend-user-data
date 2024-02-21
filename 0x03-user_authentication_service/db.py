#!/usr/bin/env python3
"""Defines dabase model"""
from sqlalchemy import create_engine, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import TypeVar, Union
from user import Base, User


class DB:
    """Defines the DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Creates a new user"""
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
            return user
        except Exception as e:
            self._session.rollback()
            return None

    def find_user_by(self, **attributes) -> User:
        """returns the first row found in the
            users table as filtered by the method’s input arguments.
        """
        try:
            result = self._session.query(User).filter_by(**attributes).first()
            if result is None:
                raise NoResultFound
            return result
        except NoResultFound as e:
            raise e
        except InvalidRequestError as e:
            raise e

    def update_user(
            self, user_id: int, **attributes
            ) -> User:
        """ takes as argument a required user_id integer and
        arbitrary keyword arguments, and returns None.
        """
        user_obj = {}
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        for key, value in attributes.items():
            if hasattr(User, key):
                user_obj[getattr(user, key)] = value
            else:
                raise ValueError(f"Invalid attribute: {key}")
        self._session.query(User).filter(User.id == user_id).update(
            user_obj,
            synchronize_session=False,
        )
        self._session.commit()
