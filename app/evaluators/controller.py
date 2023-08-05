from flask import Blueprint, render_template, redirect, abort
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from app.admin import admin_only
from app.auth import User
from app.evaluators import Evaluator
from app.projects import Project
from app import get_db_connection
from app.evaluators.forms import NewProfileForm, EditProfileForm

evaluator = Blueprint('evaluator', __name__, url_prefix='/evaluator', template_folder='templates')


@evaluator.route('/profile/<profile_id>', methods=['GET', 'POST'])
def profile(profile_id):
    db = get_db_connection()
    user = db.query(Evaluator)\
        .outerjoin(Project, Project.evaluator_id == Evaluator.id)\
        .filter(Evaluator.id == profile_id)\
        .first()
    form = EditProfileForm(user)
    if form.validate_on_submit():
        if current_user.id != user.id:
            return abort(403)
        user.name = form.name.data
        user.surname = form.surname.data
        user.bio = form.bio.data
        user.pronouns = form.pronouns.data
        user.email = form.email.data
        user.update(db, form.name.data, form.surname.data, form.email.data, form.bio.data, form.pronouns.data)
        return redirect('/evaluator/profile/' + str(user.id))
    return render_template("evaluator_profile.html", user=user, form=form)


@evaluator.route('/new', methods=['GET', 'POST'])
@login_required
@admin_only
def profile_new():
    db = get_db_connection()
    form = NewProfileForm()
    if form.validate_on_submit():
        user = Evaluator(
            name=form.name.data,
            surname=form.surname.data,
            bio=form.bio.data,
            pronouns=form.pronouns.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            grade="amateur"
        ).save(db)
        return redirect('/evaluator/profile/' + str(user.id))
    return render_template("new_evaluator.html", form=form)
