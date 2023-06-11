from app import login_manager

from sqlalchemy import Column, String

from app.main.models import CustomModel


@login_manager.user_loader
def load_user(user_id):
    """
        Returns the user corresponding the indicated id.
        param user_id: String containing the id we want to retrieve the user with.
    """
    return User.query.filter_by(id=user_id).first()


class User(CustomModel):
    __abstract__ = True
    name = Column(String(20), nullable=False)
    surname = Column(String(20), nullable=False)
    email = Column(String(20), nullable=False, unique=True)
    password = Column(String(20), nullable=False)
    profile_picture = Column(String(100))
    bio = Column(String(100))
    pronouns = Column(String(20), nullable=False)
    type = Column(String(20), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'with_polymorphic': '*',
        'polymorphic_on': type
    }

    def __init__(self, name, surname, email, password, profile_picture, bio, pronouns):
        super().__init__()
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.profile_picture = profile_picture
        self.bio = bio
        self.pronouns = pronouns

    # Saves the user to the database.
    # def save(self, db):
    #     db.session.add(self)
    #     db.session.commit()
