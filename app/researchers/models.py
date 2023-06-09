from sqlalchemy import Column, String, Integer

from app import login_manager, db

from app.auth.models import User

from app.main.models import CustomModel


class Researcher(User):
    __tablename__ = 'researchers'
    affiliation = Column(String)

    def __init__(self, name, surname, email, password, pronouns, affiliation):
        super().__init__(name, surname, email, password, pronouns, 'researchers')
        self.affiliation = affiliation