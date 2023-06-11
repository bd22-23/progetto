from sqlalchemy import Column, String

from app.auth.models import User


class Researcher(User):
    __tablename__ = 'researchers'
    affiliation = Column(String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'researcher',
        'with_polymorphic': '*'
    }

    def __init__(self, name, surname, email, password, profile_picture=None, bio=None, pronouns=None, affiliation=None):
        super().__init__(name, surname, email, password, profile_picture, bio, pronouns)
        self.affiliation = affiliation
