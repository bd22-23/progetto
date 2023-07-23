from sqlalchemy import Column, String, UUID, ForeignKey
from app.main import CustomModel


class Project(CustomModel):
    __tablename__ = 'projects'
    name = Column(String, nullable=False)
    abstract = Column(String, nullable=False)

    def __init__(self, name, abstract):
        super().__init__()
        self.name = name
        self.abstract = abstract

    def update(self, db, name, abstract):
        self.name = name
        self.abstract = abstract
        db.session.commit()
        return self


class ProjectTags(CustomModel):
    __tablename__ = 'project_tags'
    project = Column(UUID(as_uuid=True), ForeignKey('projects.id'), primary_key=True)
    tag = Column(UUID(as_uuid=True), ForeignKey('tags.id'), primary_key=True)

    def __init__(self):
        super().__init__()


class Tags(CustomModel):
    __tablename__ = 'tags'
    name = Column(String, nullable=False)

    def __init__(self, name):
        super().__init__()
        self.name = name

    def update(self, db, name):
        self.name = name
        db.session.commit()
        return self
