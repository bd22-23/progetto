from sqlalchemy import Column, String, Integer

from app import login_manager, db

from app.auth.models import User

from app.main.models import CustomModel


class Admin(User):
    __tablename__ = 'researchers'

    def __init__(self, name, surname, email, password, pronouns, affiliation):
        super().__init__(name, surname, email, password, pronouns, 'admin')

    def save(self):
        """
            Saves the user to the database.
        """
        db.session.add(self)
        db.session.commit()