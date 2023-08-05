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
        if self == Status.ACCEPTED:
            return 'Accettato'
        elif self == Status.REJECTED:
            return 'Rifiutato'
        elif self == Status.WAITING:
            return 'In Attesa'
        elif self == Status.RETURNED:
            return 'Richieste Modifiche'

    @property
    def check_icon(self):
        if self == Status.ACCEPTED:
            return 'check-circle'
        elif self == Status.REJECTED:
            return 'dash-circle'
        elif self == Status.WAITING:
            return 'clock'
        elif self == Status.RETURNED:
            return 'exclamation-circle'


class Release(CustomModel):
    __tablename__ = 'releases'
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    version = Column(String, nullable=False)
    status = Column(Enum(Status, values_callable=lambda x: [str(member.value) for member in Status]), nullable=False)
    documents = relationship('Document', backref='release', lazy=True)

    def __init__(self, project_id, version, status):
        super().__init__()
        self.project_id = project_id
        self.version = version
        self.status = status

    def update(self, db, status, version=None):
        self.version = version if version is not None else self.version
        self.status = status if status is not None else self.status
        db.commit()
        return self
