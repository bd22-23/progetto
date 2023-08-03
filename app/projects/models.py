import enum

from sqlalchemy import Column, String, UUID, ForeignKey, Enum, JSON, event
from sqlalchemy.orm import relationship, Session

from app.main import CustomModel


class Project(CustomModel):
    __tablename__ = 'projects'
    title = Column(String, nullable=False)
    abstract = Column(String, nullable=False)
    authors = relationship('Researcher', secondary='authors', backref='project_author', lazy=True)
    tags = relationship('Tag', secondary='project_tags', backref='project_tag', lazy=True)
    releases = relationship('Release', backref='project', lazy=True)
    evaluator_id = Column(UUID(as_uuid=True), ForeignKey('evaluators.id'), nullable=True)

    def __init__(self, title, abstract):
        super().__init__()
        self.title = title
        self.abstract = abstract

    def update(self, db, title, abstract):
        self.title = title
        self.abstract = abstract
        db.session.commit()
        return self


class ProjectTag(CustomModel):
    __tablename__ = 'project_tags'
    project = Column(UUID(as_uuid=True), ForeignKey('projects.id', ondelete='CASCADE'), primary_key=True)
    tag = Column(UUID(as_uuid=True), ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)

    def __init__(self, project, tag):
        super().__init__()
        self.project = project
        self.tag = tag


class Tag(CustomModel):
    __tablename__ = 'tags'
    value = Column(String, nullable=False)
    project = relationship('Project', secondary='project_tags', backref='tag', lazy=True, passive_deletes=True)

    def __init__(self, value):
        super().__init__()
        self.value = value

    def update(self, db, value):
        self.value = value
        db.session.commit()
        return self


@event.listens_for(Tag.__table__, 'after_create')
def insert_initial_values(target, connection, **kwargs):
    session = Session(bind=connection)
    session.add(Tag('scienza'))
    session.add(Tag('informatica'))
    session.add(Tag('ingegneria'))
    session.add(Tag('matematica'))
    session.add(Tag('arte'))
    session.add(Tag('musica'))
    session.add(Tag('letteratura'))
    session.add(Tag('filosofia'))
    session.add(Tag('storia'))
    session.add(Tag('geografia'))
    session.add(Tag('linguistica'))
    session.add(Tag('economia'))
    session.add(Tag('psicologia'))
    session.commit()
