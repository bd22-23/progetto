import wtforms
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from sqlalchemy import text

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    from app.auth import AbstractUser, User
    from app.evaluators import Evaluator
    from app.researchers import Researcher
    from app.admin import Admin

    app = Flask(__name__)
    app.config.from_object('config.Development')
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        with db.engine.connect() as connection:
            connection.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
            connection.execute(text("""
                CREATE OR REPLACE FUNCTION refresh_users() RETURNS TRIGGER AS $$
                BEGIN
                    REFRESH MATERIALIZED VIEW users;
                    RETURN NULL;
                END; $$ LANGUAGE plpgsql;
            """))
            connection.commit()
            db.create_all()

    from app.main.controller import main
    app.register_blueprint(main)

    from app.auth.controller import auth
    app.register_blueprint(auth)

    def is_hidden_field_filter(field):
        return isinstance(field, wtforms.HiddenField)

    app.jinja_env.globals['bootstrap_is_hidden_field'] = is_hidden_field_filter

    return app
