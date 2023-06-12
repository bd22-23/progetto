from sqlalchemy import DDL, event

from app.auth import User


class Admin(User):
    __tablename__ = 'admins'
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
        'with_polymorphic': '*'
    }

    def __init__(self, name, surname, email, password, profile_picture=None, bio=None, pronouns=None):
        super().__init__(name, surname, email, password, profile_picture, bio, pronouns)


trigger = DDL(f"""
    CREATE OR REPLACE TRIGGER refresh_{Admin.__tablename__}_trigger
    AFTER INSERT OR UPDATE OR DELETE
    ON {Admin.__tablename__}
    EXECUTE PROCEDURE refresh_users();
    """)

event.listen(Admin.__table__, 'after_create', trigger)
