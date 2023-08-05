from sqlalchemy import DDL


def create_indexes(app, db):

    indexes = [
        projects_index(),
        users_index()
    ]

    with app.app_context():
        with db.engine.connect() as connection:
            for index in indexes:
                connection.execute(index)
                connection.commit()


def projects_index():
    return DDL('''\
        CREATE INDEX IF NOT EXISTS projects_index ON projects (id, evaluator_id);
    ''')


def users_index():
    return DDL('''\
        CREATE INDEX IF NOT EXISTS users_index ON users (id, email);
    ''')
