from sqlalchemy import Column, String, UUID
from app.main import CustomModel


class Tags(CustomModel):
    __tablename__ = 'tags'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)

    def __init__(self, name):
        super().__init__()
        self.name = name

    def save(self, db):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self, db):
        db.session.delete(self)
        db.session.commit()
        return self

    def update(self, db, name):
        self.name = name
        db.session.commit()
        return self
