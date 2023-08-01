import wtforms
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import text

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    from app.auth import User
    from app.evaluators import Evaluator
    from app.researchers import Researcher, Author
    from app.admin import Admin
    from app.projects import Project, ProjectTag, Tag
    from app.releases import Release
    from app.documents import Document

    app = Flask(__name__)
    app.config.from_object('config.Development')
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        with db.engine.connect() as connection:
            connection.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
            connection.commit()
            db.create_all()

    from app.main.controller import main
    app.register_blueprint(main)

    from app.auth.controller import auth
    app.register_blueprint(auth)

    from app.projects.controller import project
    app.register_blueprint(project)

    from app.admin.controller import admin
    app.register_blueprint(admin)

    from app.evaluators.controller import evaluator
    app.register_blueprint(evaluator)

    from app.researchers.controller import researcher
    app.register_blueprint(researcher)

    from app.releases.controller import release
    app.register_blueprint(release)

    from app.documents.controller import document
    app.register_blueprint(document)

    def has_no_empty_params(rule):
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()
        return len(defaults) >= len(arguments)

    @app.route("/site-map")
    def site_map():
        links = []
        for rule in app.url_map.iter_rules():
            # Filter out rules we can't navigate to in a browser
            # and rules that require parameters
            if "GET" in rule.methods and has_no_empty_params(rule):
                from flask import url_for
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                links.append((url, rule.endpoint))
        return links

    def is_hidden_field_filter(field):
        return isinstance(field, wtforms.HiddenField)

    app.jinja_env.globals['bootstrap_is_hidden_field'] = is_hidden_field_filter

    @app.errorhandler(403)
    def handle_unauthorized(e):
        with app.app_context():
            return render_template('403.html'), 403

    return app
