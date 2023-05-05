from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Development')
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # TODO: Register blueprints

    return app