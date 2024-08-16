#!/usr/bin/env python3
"""
This module defines a SQLAlchemy model for a User.
"""
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class User(Base):
    """
    User model for the users table.
    Attributes:
        id (int): The primary key.
        email (str): The user's email, must be unique
        and not nullable.
        hashed_password (str): The hashed password for
        the user, not nullable.
        session_id (str): The session ID for the user, nullable.
        reset_token (str): The reset token for the user,
        nullable.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)


if __name__ == "__main__":
    engine = create_engine('sqlite:///example.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    new_user = User(
                    email="user@example.com",
                    hashed_password="hashedpassword123"
                    )
    session.add(new_user)
    session.commit()
