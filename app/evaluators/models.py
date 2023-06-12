from sqlalchemy import Column, String, Integer, event, DDL

from app.auth.models import User


class Evaluator(User):
    __tablename__ = 'evaluators'
    grade = Column(String(20))
    __mapper_args__ = {
        'polymorphic_identity': 'evaluator',
        'with_polymorphic': '*'
    }

    def __init__(self, name, surname, email, password, profile_picture=None, bio=None, pronouns=None, grade=None):
        super().__init__(name, surname, email, password, profile_picture, bio, pronouns)
        self.grade = grade


trigger = DDL(f"""
    CREATE OR REPLACE TRIGGER refresh_{Evaluator.__tablename__}_trigger
    AFTER INSERT OR UPDATE OR DELETE
    ON {Evaluator.__tablename__}
    EXECUTE PROCEDURE refresh_users();
    """)

event.listen(Evaluator.__table__, 'after_create', trigger)
