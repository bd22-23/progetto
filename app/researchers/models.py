from sqlalchemy import Column, String, ForeignKey, UUID, Date
import datetime

from sqlalchemy.orm import relationship

from app.auth.models import User
from app.main import CustomModel


class Researcher(User):
    __tablename__ = 'researchers'
    id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    affiliation = Column(String, nullable=False)
    role = Column(String)
    pronouns = Column(String)
    projects = relationship('Project', secondary='authors', backref='researcher', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'researcher',
        'with_polymorphic': '*'
    }

    def __init__(self, name, surname, email, password, affiliation, role=None, pronouns=None):
        super().__init__(name, surname, email, password)
        self.affiliation = affiliation
        self.role = role
        self.pronouns = pronouns

    def update(self, db, name, surname, email, affiliation, role, pronouns):
        self.name = name if name is not None else self.name
        self.surname = surname if surname is not None else self.surname
        self.email = email if email is not None else self.email
        self.affiliation = affiliation if affiliation is not None else self.affiliation
        self.role = role if role is not None else self.role
        self.pronouns = pronouns if pronouns is not None else self.pronouns
        db.session.commit()
        return self


class Author(CustomModel):
    __tablename__ = 'authors'
    project = Column(UUID(as_uuid=True), ForeignKey('projects.id'), primary_key=True)
    researcher = Column(UUID(as_uuid=True), ForeignKey('researchers.id'), primary_key=True)

    def __init__(self, project, researcher):
        super().__init__()
        self.project = project
        self.researcher = researcher


