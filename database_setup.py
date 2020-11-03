import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
class User(Base):
     __tablename__ = 'user'
     id = Column(Integer, primary_key=True)
     name = Column(String(250), nullable=False)
     email = Column(String(250), nullable=False)

class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

# Serialize function for sending JSON objects in a serializable format
    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }


class Book(Base):
    __tablename__ = 'book'

    title = Column(String(50), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship(Author)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

# Serialize function for sending JSON objects in a serializable format
    @property
    def serialize(self):

        return {
            'title': self.title,
            'description': self.description,
            'id': self.id,
        }


engine = create_engine('sqlite:///books.db')
Base.metadata.create_all(engine)
