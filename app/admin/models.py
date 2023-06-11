from app.auth.models import User


class Admin(User):
    __tablename__ = 'admins'
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
        'with_polymorphic': '*'
    }

    def __init__(self, name, surname, email, password, profile_picture=None, bio=None, pronouns=None):
        super().__init__(name, surname, email, password, profile_picture, bio, pronouns)
