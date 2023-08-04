from sqlalchemy import text


def create_roles(app, db):
    with app.app_context():
        with db.engine.connect() as connection:
            with open('app/roles.sql', 'r') as file:
                query = text(file.read())
                connection.execute(query)
                connection.commit()
