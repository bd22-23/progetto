from sqlalchemy import select, literal, union_all

from app.admin import Admin
from app.evaluators import Evaluator
from app.researchers import Researcher
from app.utils import MaterializedView, create_mat_view


class UserMV(MaterializedView):
    evaluator_query = select(
        Evaluator.name,
        Evaluator.surname,
        Evaluator.email,
        Evaluator.password,
        Evaluator.profile_picture,
        Evaluator.bio,
        Evaluator.pronouns,
        literal('evaluators').label('from_table')
    ).select_from(Evaluator)

    researcher_query = select(
        Researcher.name,
        Researcher.surname,
        Researcher.email,
        Researcher.password,
        Researcher.profile_picture,
        Researcher.bio,
        Researcher.pronouns,
        literal('researchers').label('from_table')
    ).select_from(Researcher)

    admin_query = select(
        Admin.name,
        Admin.surname,
        Admin.email,
        Admin.password,
        Admin.profile_picture,
        Admin.bio,
        Admin.pronouns,
        literal('admin').label('from_table')
    ).select_from(Admin)

    __table__ = create_mat_view(
        "users",
        union_all(evaluator_query, researcher_query, admin_query)
    )
