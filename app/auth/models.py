from flask_login import UserMixin
from sqlalchemy import Column, String

from app.main import CustomModel


class User(CustomModel, UserMixin):
    __abstract__ = True
    name = Column(String(20), nullable=False)
    surname = Column(String(20), nullable=False)
    email = Column(String(20), nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    profile_picture = Column(String(100))
    bio = Column(String(100))
    pronouns = Column(String(20))

    def __init__(self, name, surname, email, password, profile_picture, bio, pronouns):
        super().__init__()
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.profile_picture = profile_picture
        self.bio = bio
        self.pronouns = pronouns
