from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship
from app.main import CustomModel


class Project(CustomModel):
    __tablename__ = 'projects'
    title = Column(String, nullable=False)
    abstract = Column(String, nullable=False)
    authors = relationship('Researcher', secondary='authors', backref='project_author', lazy=True, passive_deletes=True)
    tags = relationship('Tag', secondary='project_tags', backref='project_tag', lazy=True, passive_deletes=True)

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

    def __init__(self, name):
        super().__init__()
        self.name = name

    def update(self, db, name):
        self.name = name
        db.session.commit()
        return self
