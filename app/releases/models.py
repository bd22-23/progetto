from sqlalchemy import String, Column, JSON, UUID, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.main import CustomModel
from app.projects.models import Status


class Document(CustomModel):
    __tablename__ = 'documents'
    title = Column(String, nullable=False)
    path = Column(String, nullable=False)
    annotations = Column(JSON, nullable=False)
    release = Column(UUID(as_uuid=True), ForeignKey('releases.id'), nullable=False)

    def __init__(self, title, path, annotations=None):
        super().__init__()
        self.name = title
        self.path = path
        self.annotations = annotations


class Release(CustomModel):
    __tablename__ = 'releases'
    project = Column(UUID(as_uuid=True), ForeignKey('projects.id'), nullable=False)
    version = Column(String, nullable=False)
    status = Column(Enum(Status, values_callable=lambda x: [str(member.value) for member in Status]), nullable=False)
    documents = relationship('Document', backref='releases', lazy=True)

    def __init__(self, project, version, status):
        super().__init__()
        self.project = project
        self.version = version
        self.status = status
