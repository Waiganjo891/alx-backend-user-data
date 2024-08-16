#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from user import Base, User


class DB:
    """
    DB class
    """
    def __init__(self) -> None:
        """
        Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a user to the database
        Args:
            email (str): The user's email.
            hashed_password (str): The user's hashed password.
        Returns:
            User: The created User object.
        """
        new_user = User(
                        email=email,
                        hashed_password=hashed_password
                        )
        session = self._session
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by arbitrary keyword arguments
        Args:
            kwargs: Arbitrary keyword arguments to filter
            the user.
        Returns:
            User: The first user that matches the criteria.
        Raises:
            NoResultFound: If no user is found.
            InvalidRequestError: If query is invalid.
        """
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound("No user found with the given criteria.")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments.")
