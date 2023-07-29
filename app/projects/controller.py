from flask import Blueprint, render_template, url_for, redirect, request
from flask_login import current_user, login_required

from app import db
from app.researchers import Author, Researcher
from app.projects import Project, ProjectTag, Tag
from app.projects.forms import NewProjectForm, EditProjectForm

project = Blueprint('project', __name__, url_prefix='/project', template_folder='templates')


@project.route('/list', methods=['GET', 'POST'])
def list():
    tag = request.args.get('tag')
    query = Project.query \
        .join(Author, Author.project == Project.id) \
        .join(ProjectTag, ProjectTag.project == Project.id) \
        .join(Tag, Tag.id == ProjectTag.tag) \
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
        .filter(Project.id == project_id) \
        .first()
    tags = Tag.query.all()
    users = Researcher.query.all()
    form = EditProjectForm(tags, proj, users)
    if form.validate_on_submit():
        proj.title = form.title.data
        proj.abstract = form.abstract.data
        proj.save(db)
        ProjectTag.query.filter_by(project=proj.id).delete()
        for tag in form.tags.data:
            ProjectTag(proj.id, tag).save(db)
        Author.query.filter_by(project=proj.id).delete()
        for author in form.authors.data:
            Author(proj.id, author).save(db)
        return redirect(url_for('project.view', project_id=proj.id))
    return render_template('project_view.html', project=proj, tags=tags, form=form)


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
        for tag in form.tags.data:
            ProjectTag(proj.id, tag).save(db)
        return redirect(url_for('project.view', project_id=proj.id))
    return render_template('project_new.html', form=form)


@login_required
@project.route('/delete/<project_id>', methods=['GET', 'POST'])
def delete(project_id):
    proj = Project.query.filter_by(id=project_id).first()
    proj.delete(db)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DELETED")
    return redirect(url_for('project.list'))
