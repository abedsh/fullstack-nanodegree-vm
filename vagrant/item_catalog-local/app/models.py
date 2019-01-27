from app import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import json
from flask import jsonify, make_response
from flask_login import UserMixin


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    items = relationship("Item", lazy='subquery')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'items': self.serialize_items
        }

    @property
    def serialize_items(self):

        return [item.serialize for item in self.items]


class Item(Base):
    __tablename__ = 'item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    user_id = Column(String(64))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category, lazy='subquery')

    @property
    def serialize(self):
        return {
              'id': self.id,
              'name': self.name,
              'description': self.description,
              'userId':self.user_id
        }

    def __init__(self, id=0, name="", description="", idCategory=0,userId=""):
        self.id = id
        self.name = name
        self.description = description
        self.category_id = idCategory
        self.user_id = userId

    def toMappedValues(self):
        values = {}
        for attr, value in self.__dict__.iteritems():
            if attr != "id" and attr != "_sa_instance_state":
                    values[str(attr)] = str(value)

        return values


# user class for the to be used with the login manager https://flask-login.readthedocs.io/en/latest/
class User(UserMixin):
        def __init__(self, id, name, picture, email):
            self.id = id
            self.name = name
            self.picture = picture
            self.email = email

        def is_active(self):
            # Here you should write whatever the code is
            # that checks the database if your user is active
            return True

        def is_authenticated(self):
            return True

        def get_id(self):
            return self.id
