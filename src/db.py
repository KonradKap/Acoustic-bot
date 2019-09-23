from contextlib import contextmanager

import sqlalchemy
import sqlalchemy.exc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, User


database_name = 'meme.db'
database = create_engine(f'sqlite:///{database_name}')
Base.metadata.create_all(database)
Session = sessionmaker(bind=database)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except sqlalchemy.exc.SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()


def add_user(user):
    try:
        with session_scope() as session:
            session.add(user)
    except sqlalchemy.exc.IntegrityError:
        return False
    return True


def remove_user(userID):
    with session_scope() as session:
        session.query(User).filter(User.id == userID).delete()


def get_user(userID):
    with session_scope() as session:
        user = session.query(User).get(userID)
        if user:
            session.expunge(user)
        return user


def get_users():
    with session_scope() as session:
        users = session.query(User).all()
        for user in users:
            session.expunge(user)
        return users


def update_pair(giver, taker):
    with session_scope() as session:
        giver = session.query(User).get(giver.id)
        taker = session.query(User).get(taker.id)
        giver.taker_chat_id = taker.chat_id
        taker.giver_chat_id = giver.chat_id
