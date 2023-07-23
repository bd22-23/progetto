import datetime
from sqlalchemy import Column, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app import db


class Authors(db.Model):
    __tablename__ = 'authors'
    project = Column(UUID(as_uuid=True), ForeignKey('projects.id'), primary_key=True)
    researcher = Column(UUID(as_uuid=True), ForeignKey('researchers.id'), primary_key=True)
    created_at = Column(Date, nullable=False, default=datetime.datetime.now)

    def __init__(self):
        super().__init__()

    def save(self, db):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self, db):
        db.session.delete(self)
        db.session.commit()
        return self

    def new(self, db, project, researcher):
        self.project = project
        self.researcher = researcher
        db.session.add(self)
        db.session.commit()
        return self
