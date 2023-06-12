import wtforms
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from sqlalchemy import text

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    from app.auth.models import User
    from app.evaluators.models import Evaluator
    from app.researchers.models import Researcher
    from app.admin.models import Admin
    from app.auth.materialized_view import UserMV

    app = Flask(__name__)
    app.config.from_object('config.Development')
    db.init_app(app)

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
