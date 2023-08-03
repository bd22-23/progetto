from sqlalchemy import Column, String, JSON, UUID, ForeignKey

from app.main import CustomModel


class Document(CustomModel):
    __tablename__ = 'documents'
    path = Column(String, nullable=False)
    annotations = Column(JSON, nullable=False)
    release_id = Column(UUID(as_uuid=True), ForeignKey('releases.id'), nullable=False)

    def __init__(self, path, release_id, annotations=None):
        super().__init__()
        self.path = path
        self.release_id = release_id
        self.annotations = annotations
        