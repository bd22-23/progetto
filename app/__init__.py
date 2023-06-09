from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Development')
    db.init_app(app)

    # with app.app_context():
    #     db.create_all()

    # TODO: Register blueprints
    from app.main.controller import main
    app.register_blueprint(main)

    from app.auth.controller import auth
    app.register_blueprint(auth)

    from wtforms import HiddenField

    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)

    app.jinja_env.globals['bootstrap_is_hidden_field'] = is_hidden_field_filter

    return app
