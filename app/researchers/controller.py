from flask import Blueprint, render_template, request, redirect

from app.auth import User
from app.researchers import Researcher

from app import db

researcher = Blueprint('researcher', __name__, url_prefix='/researcher', template_folder='templates')


@researcher.route('/profile/<profile_id>')
def profile(profile_id):
    user = Researcher.query.join(User, User.id == Researcher.id).filter_by(id=profile_id).first()
    return render_template("researcher_profile.html", user=user)


@researcher.route('/profile/update/<profile_id>', methods=['POST'])
def profile_update(profile_id):
    res = Researcher.query.filter_by(id=profile_id).first()
    res.update(db, request.form.get("name"), request.form.get("surname"), request.form.get("email"),
               request.form.get("affiliation"), request.form.get("role"), request.form.get("pronouns"))
    return redirect('/researcher/profile/' + str(profile_id))
