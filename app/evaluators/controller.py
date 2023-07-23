from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash

from app.auth import User
from app.evaluators import Evaluator

from app import db
from app.evaluators.forms import NewProfileForm

evaluator = Blueprint('evaluator', __name__, url_prefix='/evaluator', template_folder='templates')


@evaluator.route('/profile/<profile_id>')
def profile(profile_id):
    user = Evaluator.query.join(User, User.id == Evaluator.id).filter_by(id=profile_id).first()
    return render_template("evaluator_profile.html", user=user)


@evaluator.route('/profile/update/<profile_id>', methods=['POST'])
def profile_update(profile_id):
    eva = Evaluator.query.filter_by(id=profile_id).first()
    eva.update(db, request.form.get("name"), request.form.get("surname"), request.form.get("email"),
               request.form.get("bio"), request.form.get("pronouns"), request.form.get("password"))
    return redirect('/evaluator/profile/' + str(profile_id))


@evaluator.route('/new', methods=['GET', 'POST'])
def profile_new():
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
