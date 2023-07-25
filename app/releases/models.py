import enum

from sqlalchemy import String, Column, JSON, UUID, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.main import CustomModel


class Status(enum.Enum):
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    WAITING = 'waiting'
    RETURNED = 'returned'

    @property
    def label(self):
        if self.value == 'accepted':
            return 'Accettato'
        elif self.value == 'rejected':
            return 'Rifiutato'
        elif self.value == 'waiting':
            return 'In Attesa'
        elif self.value == 'returned':
            return 'Richieste Modifiche'

    @property
    def check_icon(self):
        if self.value == 'accepted':
            return 'check'
        elif self.value == 'rejected':
            return 'dash'
        elif self.value == 'waiting':
            return 'clock'
        elif self.value == 'returned':
            return 'exclamation'


class Release(CustomModel):
    __tablename__ = 'releases'
    project = Column(UUID(as_uuid=True), ForeignKey('projects.id'), nullable=False)
    version = Column(String, nullable=False)
    status = Column(Enum(Status, values_callable=lambda x: [str(member.value) for member in Status]), nullable=False)
    documents = relationship('Document', backref='release', lazy=True)

    def __init__(self, project, version, status):
        super().__init__()
        self.project = project
        self.version = version
        self.status = status
