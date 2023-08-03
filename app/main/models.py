from sqlalchemy import Column, DateTime, func
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
    created_at = Column(DateTime, server_default=func.current_timestamp(), nullable=False)

    def __init__(self):
        pass

    def save(self, database):
        database.add(self)
        database.commit()
        return self

    def delete(self, database):
        database.delete(self)
        database.commit()
        return self

    def __repr__(self):
        return f"<Model {self.id}"
