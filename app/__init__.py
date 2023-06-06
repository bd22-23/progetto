from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Production')
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # TODO: Register blueprints
    from app.main.controller import main
    app.register_blueprint(main)

    return app
