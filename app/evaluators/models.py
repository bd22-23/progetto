from sqlalchemy import Column, String, Integer

from app import login_manager, db

from app.auth.models import User

from app.main.models import CustomModel


class Evaluators(User):
    __tablename__ = 'researchers'
    grade = Column(String)

    def __init__(self, name, surname, email, password, pronouns, grade):
        super().__init__(name, surname, email, password, pronouns, 'evaluators')
        self.grade = grade