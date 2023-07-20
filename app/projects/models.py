from sqlalchemy import Column, String, UUID
from app.main import CustomModel


class Project(CustomModel):
    __tablename__ = 'projects'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    abstract = Column(String, nullable=False)

    def __init__(self, name, abstract):
        super().__init__()
        self.name = name
        self.abstract = abstract

    def save(self, db):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self, db):
        db.session.delete(self)
        db.session.commit()
        return self

    def update(self, db, name, abstract):
        self.name = name
        self.abstract = abstract
        db.session.commit()
        return self
