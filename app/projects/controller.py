from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user, login_required

from app import db
from app.auth import User
from app.researchers import Author
from app.projects import Project, ProjectTag, Tag
from app.projects.forms import NewProjectForm
from app.projects.tables import ProjectTable

project = Blueprint('project', __name__, url_prefix='/project', template_folder='templates')


@project.route('/list', methods=['GET', 'POST'])
def list():
    projects = Project.query.all()
    table = ProjectTable(projects)
    return render_template('project_list.html', project_table=table)


@project.route('/view/<project_id>', methods=['GET', 'POST'])
def view(project_id):
    proj = Project.query.filter_by(id=project_id).first()
    tag_query = db.session.query(Tag.name).join(ProjectTag, ProjectTag.tag == Tag.id).filter(
        ProjectTag.project == project_id).all()
    tags = [tag[0] for tag in tag_query]
    author_query = db.session.query(User.id, User.name, User.surname).join(
        Author, Author.researcher == User.id).filter(Author.project == project_id).all()
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
