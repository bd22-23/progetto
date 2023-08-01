import enum
from sqlalchemy import Column, String, Enum, ForeignKey, UUID
from app.auth.models import User


class Grade(enum.Enum):
    AMATEUR = "amateur"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"


class Evaluator(User):
    __tablename__ = 'evaluators'
    id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    bio = Column(String)
    pronouns = Column(String)
    grade = Column(Enum(Grade, values_callable=lambda x: [str(member.value) for member in Grade]), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'evaluator',
        'with_polymorphic': '*'
    }

    def __init__(self, name, surname, email, password, grade, bio=None, pronouns=None):
        super().__init__(name, surname, email, password)
        self.grade = grade
        self.bio = bio
        self.pronouns = pronouns

    def update(self, db, name, surname, email, bio, pronouns, grade=None):
        self.name = name if name is not None else self.name
        self.surname = surname if surname is not None else self.surname
        self.email = email if email is not None else self.email
        self.grade = grade if grade is not None else self.grade
        self.bio = bio if bio is not None else self.bio
        self.pronouns = pronouns if pronouns is not None else self.pronouns
        db.session.commit()
        return self
