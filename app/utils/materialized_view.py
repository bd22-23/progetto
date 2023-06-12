from abc import ABC
from sqlalchemy.ext import compiler
from sqlalchemy.schema import DDLElement, PrimaryKeyConstraint

from app import db


class CreateMaterializedView(ABC, DDLElement):
    """
    Create a materialized view with the given name from the given selectable.
    """
    def __init__(self, name, selectable):
        self.name = name
        self.selectable = selectable


@compiler.compiles(CreateMaterializedView)
def compile(element, compiler):
    return 'CREATE MATERIALIZED VIEW IF NOT EXISTS %s AS %s' % (
        element.name,
        compiler.sql_compiler.process(element.selectable, literal_binds=True),
    )


def create_mat_view(name, selectable, metadata=db.metadata):
    """
    Creates a materialized view from a selectable.
    :param name: name of the view
    :param selectable: a SQLAlchemy selectable (e.g. a select() statement)
    :param metadata: the metadata object to which the view should be added
    :return: the view object
    """
    _mt = db.MetaData()
    t = db.Table(name, _mt)
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
    """
    Refreshes a materialized view.
    :param name: name of the view
    :param concurrently: whether to refresh concurrently
    :return: None
    """
    db.session.flush()
    _con = 'CONCURRENTLY ' if concurrently else ''
    db.session.execute('REFRESH MATERIALIZED VIEW ' + _con + name)


def refresh_all_mat_views(concurrently=True):
    """
    Refreshes all materialized views. Currently, views are refreshed in
    non-deterministic order, so view definitions can't depend on each other.
    """
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
