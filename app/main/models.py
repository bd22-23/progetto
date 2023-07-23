import datetime
from sqlalchemy import Column, Date, func
from sqlalchemy.dialects.postgresql import UUID
from app import db


class CustomModel(db.Model):
    """
    Represents every model in the db.
    """
    __abstract__ = True
    id = Column(UUID(as_uuid=True),
                server_default=func.public.uuid_generate_v4(),
                nullable=False, primary_key=True)
    created_at = Column(Date, nullable=False, default=datetime.datetime.now)

    def __init__(self):
        pass

    def __repr__(self):
        return f"<Model {self.id}"
