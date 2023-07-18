from flask import Blueprint, render_template, request, redirect

from app.auth import User
from app.evaluators import Evaluator


from app import db
from app.evaluators.models import Grade

evaluator = Blueprint('evaluator', __name__, url_prefix='/evaluator', template_folder='templates')


@evaluator.route('/profile/<profile_id>')
def profile(profile_id):
    user = Evaluator.query.join(User, User.id == Evaluator.id).filter_by(id=profile_id).first()
    print("---------------------------------------------")
    grade = user.grade.value
    print(grade)
    return render_template("evaluator_profile.html", user=user)


@evaluator.route('/profile/update/<profile_id>', methods=['POST'])
def profile_update(profile_id):
    eva = Evaluator.query.filter_by(id=profile_id).first()
    eva.update(db, request.form.get("name"), request.form.get("surname"), request.form.get("email"),
               request.form.get("bio"), request.form.get("pronouns"))
    return redirect('/evaluator/profile/' + str(profile_id))
