from sqlalchemy import Column, UUID, ForeignKey

from app.auth.models import User


class Admin(User):
    __tablename__ = 'admins'
    id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
        'with_polymorphic': '*'
    }

    def __init__(self, name, surname, email, password):
        super().__init__(name, surname, email, password)
