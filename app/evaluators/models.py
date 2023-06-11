from sqlalchemy import Column, String, Integer

from app.auth.models import User


class Evaluator(User):
    __tablename__ = 'evaluators'
    grade = Column(String(20))
    __mapper_args__ = {
        'polymorphic_identity': 'evaluator',
        'with_polymorphic': '*'
    }

    def __init__(self, name, surname, email, password, profile_picture=None, bio=None, pronouns=None, grade=None):
        super().__init__(name, surname, email, password, profile_picture, bio, pronouns)
        self.grade = grade
