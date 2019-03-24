from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from app import db

Base = declarative_base()


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))

    # Custom User Payload
    def get_security_payload(self):
        return {
            'id': self.id,
            'name': self.username,
        }

    # __str__ is required by Flask-Admin, so we can have human-readable values for the email when editing a User.
    def __str__(self):
        return self.email
