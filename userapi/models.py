from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper
from database import metadata, db_session

class User(object):
    query = db_session.query_property()

    def __init__(self, id=None, name=None, email=None, password=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)

users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), unique=True),
    Column('email', String(120), unique=True),
    Column('password', String(50))
)
mapper(User, users)
