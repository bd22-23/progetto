from flask_login import UserMixin

from sqlalchemy import Column, String

from app import login_manager
from app.main import CustomModel


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(CustomModel, UserMixin):
    __tablename__ = 'users'
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    type = Column(String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'with_polymorphic': '*',
        'polymorphic_on': type
    }

    def __init__(self, name, surname, email, password):
        super().__init__()
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
