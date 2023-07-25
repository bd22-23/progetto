from sqlalchemy import Column, Date, func, DateTime
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
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __init__(self):
        pass

    def save(self, database):
        database.session.add(self)
        database.session.commit()
        return self

    def delete(self, database):
        database.session.delete(self)
        database.session.commit()
        return self

    def __repr__(self):
        return f"<Model {self.id}"
