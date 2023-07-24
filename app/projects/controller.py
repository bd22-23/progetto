import os

from flask import Blueprint, render_template, url_for, redirect, request, current_app
from flask_login import current_user, login_required
from sqlalchemy import desc

from app import db
from app.releases import Release
from app.researchers import Author
from app.projects import Project, ProjectTag, Tag
from app.projects.forms import NewProjectForm

project = Blueprint('project', __name__, url_prefix='/project', template_folder='templates')


@project.route('/list', methods=['GET', 'POST'])
def list():
    tag = request.args.get('tag')
    query = Project.query \
        .join(Author, Author.project == Project.id) \
        .join(ProjectTag, ProjectTag.project == Project.id) \
        .join(Tag, Tag.id == ProjectTag.tag) \
        .outerjoin(Release, Release.project == Project.id) \
        .filter(ProjectTag.project == Project.id)
    if tag:
        query = query.filter(Tag.value == tag)
    projects = query.all()
    return render_template('project_list.html', projects=projects, tag=tag)


@project.route('/view/<project_id>', methods=['GET', 'POST'])
def view(project_id):
    proj = Project.query \
        .join(Author, Author.project == Project.id) \
        .join(ProjectTag, ProjectTag.project == Project.id) \
        .join(Tag, Tag.id == ProjectTag.tag) \
        .outerjoin(Release, Release.project == Project.id) \
        .filter(Project.id == project_id) \
        .order_by(desc(Release.version))\
        .first()
    return render_template('project_view.html', project=proj)


@login_required
@project.route('/new', methods=['GET', 'POST'])
def new():
    tags = Tag.query.all()
    form = NewProjectForm(tags)
    if form.validate_on_submit():
        proj = Project(
            title=form.title.data,
            abstract=form.abstract.data
        ).save(db)
        Author(proj.id, current_user.id).save(db)
        os.makedirs(os.path.dirname(current_app.config['UPLOAD_FOLDER'] + '/' + str(proj.id) + '/'), exist_ok=True)
        for tag in form.tags.data:
            ProjectTag(proj.id, tag).save(db)
        return redirect(url_for('project.view', project_id=proj.id))
    return render_template('project_new.html', form=form)
