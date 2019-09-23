from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True)
    username = Column(String)
    chat_id = Column(Integer, unique=True)
    giver_chat_id = Column(Integer, unique=True, default=None)
    taker_chat_id = Column(Integer, unique=True, default=None)

    def __init__(self, id, username, chat_id):
        self.id = id
        self.username = username
        self.chat_id = chat_id

    def __repr__(self):
        return (f"<User(id={self.id},"
                f"username={self.username}, "
                f"chat_id={self.chat_id}, "
                f"giver_chat_id={self.giver_chat_id}, "
                f"taker_chat_id={self.taker_chat_id})>")
