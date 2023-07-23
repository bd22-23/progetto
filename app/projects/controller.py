from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user, login_required

from app import db
from app.auth import User
from app.authors import Authors
from app.project_tags import ProjectTags
from app.projects import Project
from app.projects.forms import NewProjectForm
from app.projects.tables import ProjectTable
from app.tags import Tags

project = Blueprint('project', __name__, url_prefix='/project', template_folder='templates')


@project.route('/list', methods=['GET', 'POST'])
def project_list():
    projects = Project.query.all()
    table = ProjectTable(projects)
    return render_template('project_list.html', project_table=table)


@project.route('/view/<project_id>', methods=['GET', 'POST'])
def project_view(project_id):
    proj = Project.query.filter_by(id=project_id).first()
    tag_query = db.session.query(Tags.name).join(ProjectTags, ProjectTags.tag == Tags.id).filter(
        ProjectTags.project == project_id).all()
    tags = [tag[0] for tag in tag_query]
    author_query = db.session.query(User.id, User.name, User.surname).join(
        Authors, Authors.researcher == User.id).filter(Authors.project == project_id).all()
    authors = [
        {
            'id': str(author.id),
            'name': author.name,
            'surname': author.surname
        } for author in author_query
    ]
    return render_template('project_view.html', project=proj, tags=tags, authors=authors)


@login_required
@project.route('/new', methods=['GET', 'POST'])
def project_new():
    tags = Tags.query.all()
    form = NewProjectForm(tags)
    if form.validate_on_submit():
        proj = Project(
            name=form.name.data,
            abstract=form.abstract.data
        ).save(db)
        Authors().new(db, proj.id, current_user.id)
        for tag in form.tags.data:
            ProjectTags().new(db, proj.id, tag)
        return redirect(url_for('project.project_view', project_id=proj.id))
    return render_template('project_new.html', form=form)
