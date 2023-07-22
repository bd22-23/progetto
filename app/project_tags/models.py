import datetime
from sqlalchemy import Column, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app import db


class ProjectTags(db.Model):
    __tablename__ = 'project_tags'
    project = Column(UUID(as_uuid=True), ForeignKey('projects.id') ,primary_key=True)
    tag = Column(UUID(as_uuid=True), ForeignKey('tags.id'), primary_key=True)
    created_at = Column(Date, nullable=False, default=datetime.datetime.now)

    def __init__(self, name):
        super().__init__()
        self.name = name

    def save(self, db):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self, db):
        db.session.delete(self)
        db.session.commit()
        return self
