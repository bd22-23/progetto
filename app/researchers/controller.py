from flask import Blueprint, render_template, redirect
from app.auth import User
from app.projects import Project, ProjectTag, Tag
from app.researchers import Researcher, Author
from app import db
from app.researchers.forms import EditResearcherForm

researcher = Blueprint('researcher', __name__, url_prefix='/researcher', template_folder='templates')


@researcher.route('/profile/<profile_id>', methods=['GET', 'POST'])
def profile(profile_id):
    user = Researcher.query.join(User, User.id == Researcher.id).filter_by(id=profile_id).first()
    form = EditResearcherForm(user)
    proj = Project.query \
        .join(Author, Author.project == Project.id) \
        .join(ProjectTag, ProjectTag.project == Project.id) \
        .join(Tag, Tag.id == ProjectTag.tag) \
        .filter(Author.researcher == user.id) \
        .all()
    if form.validate_on_submit():
        user.update(db, form.name.data, form.surname.data, form.email.data, form.affiliation.data,
                    form.role.data, form.pronouns.data)
        return redirect('/researcher/profile/' + str(user.id))
    return render_template("researcher_profile.html", user=user, form=form, projects=proj)
