from sqlalchemy import Column, String, Integer
from app import login_manager, db
from app.main.models import CustomModel


@login_manager.user_loader
def load_user(user_id):
    """
        Returns the user corresponding the indicated id.
        param user_id: String containing the id we want to retrieve the user with.
    """
    return User.query.filter_by(id=user_id).first()

class User(CustomModel):
    __tablename__ = 'users'
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    profile_picture = Column(String)
    bio = Column(String)
    pronouns = Column(String, nullable=False)
    from_table = Column(Integer, nullable=False)

    def __init__(self, name, surname, email, password, pronouns, from_table):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.pronouns = pronouns
        self.from_table = from_table

    def save(self):
        """
            Saves the user to the database.
        """
        db.session.add(self)
        db.session.commit()
