from app import db

from sqlalchemy.ext import compiler
from sqlalchemy.schema import DDLElement, PrimaryKeyConstraint

from app.admin.models import Admin
from app.evaluators.models import Evaluator
from app.researchers.models import Researcher


class CreateMaterializedView(DDLElement):
    def __init__(self, name, selectable):
        self.name = name
        self.selectable = selectable


@compiler.compiles(CreateMaterializedView)
def compile(element, compiler, **kw):
    # Could use "CREATE OR REPLACE MATERIALIZED VIEW..."
    # but I'd rather have noisy errors
    return 'CREATE MATERIALIZED VIEW %s AS %s' % (
        element.name,
        compiler.sql_compiler.process(element.selectable, literal_binds=True),
    )


def create_mat_view(name, selectable, metadata=db.metadata):
    _mt = db.MetaData()  # temp metadata just for initial Table object creation
    t = db.Table(name, _mt)  # the actual mat view class is bound to db.metadata
    for c in selectable.c:
        t.append_column(db.Column(c.name, c.type, primary_key=c.primary_key))

    if not (any([c.primary_key for c in selectable.c])):
        t.append_constraint(PrimaryKeyConstraint(*[c.name for c in selectable.c]))

    db.event.listen(
        metadata, 'after_create',
        CreateMaterializedView(name, selectable)
    )

    @db.event.listens_for(metadata, 'after_create')
    def create_indexes(target, connection, **kw):
        for idx in t.indexes:
            idx.create(connection)

    db.event.listen(
        metadata, 'before_drop',
        db.DDL('DROP MATERIALIZED VIEW IF EXISTS ' + name)
    )
    return t


def refresh_mat_view(name, concurrently):
    # since session.execute() bypasses auto flush, must manually flush in order
    # to include newly-created/modified objects in the refresh
    db.session.flush()
    _con = 'CONCURRENTLY ' if concurrently else ''
    db.session.execute('REFRESH MATERIALIZED VIEW ' + _con + name)


def refresh_all_mat_views(concurrently=True):
    """Refreshes all materialized views. Currently, views are refreshed in
    non-deterministic order, so view definitions can't depend on each other."""
    mat_views = db.inspect(db.engine).get_view_names(include='materialized')
    for v in mat_views:
        refresh_mat_view(v, concurrently)


class MaterializedView(db.Model):
    __abstract__ = True

    @classmethod
    def refresh(cls, concurrently=True):
        """
        Refreshes the current materialized view
        """
        refresh_mat_view(cls.__table__.fullname, concurrently)


class UserMV(MaterializedView):
    evaluator_records = db.session.query(
        Evaluator.id,
        Evaluator.name,
        Evaluator.surname,
        Evaluator.email,
        Evaluator.password,
        Evaluator.profile_picture,
        Evaluator.bio,
        Evaluator.pronouns
    )

    researcher_records = db.session.query(
        Researcher.id,
        Researcher.name,
        Researcher.surname,
        Researcher.email,
        Researcher.password,
        Researcher.profile_picture,
        Researcher.bio,
        Researcher.pronouns
    )

    admin_records = db.session.query(
        Admin.id,
        Admin.name,
        Admin.surname,
        Admin.email,
        Admin.password,
        Admin.profile_picture,
        Admin.bio,
        Admin.pronouns
    )

    __table__ = create_mat_view(
        "users",
        db.union_all(evaluator_records, researcher_records, admin_records)
    )
