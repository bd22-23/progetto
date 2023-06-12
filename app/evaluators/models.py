from sqlalchemy import Column, String, event, DDL

from app.auth import User


class Evaluator(User):
    __tablename__ = 'evaluators'
    grade = Column(String(20))

    def __init__(self, name, surname, email, password, profile_picture=None, bio=None, pronouns=None, grade=None):
        super().__init__(name, surname, email, password, profile_picture, bio, pronouns)
        self.grade = grade

    def save(self, db):
        db.session.add(self)
        db.session.commit()
        return self


trigger = DDL(f"""
    CREATE OR REPLACE TRIGGER refresh_{Evaluator.__tablename__}_trigger
    AFTER INSERT OR UPDATE OR DELETE
    ON {Evaluator.__tablename__}
    EXECUTE PROCEDURE refresh_users();
    """)

event.listen(Evaluator.__table__, 'after_create', trigger)
