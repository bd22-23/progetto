from sqlalchemy import Column, String, DDL, event

from app.auth import User


class Researcher(User):
    __tablename__ = 'researchers'
    affiliation = Column(String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'researcher',
        'with_polymorphic': '*'
    }

    def __init__(self, name, surname, email, password, profile_picture=None, bio=None, pronouns=None, affiliation=None):
        super().__init__(name, surname, email, password, profile_picture, bio, pronouns)
        self.affiliation = affiliation


trigger = DDL(f"""
    CREATE OR REPLACE TRIGGER refresh_{Researcher.__tablename__}_trigger
    AFTER INSERT OR UPDATE OR DELETE
    ON {Researcher.__tablename__}
    EXECUTE PROCEDURE refresh_users();
    """)

event.listen(Researcher.__table__, 'after_create', trigger)
