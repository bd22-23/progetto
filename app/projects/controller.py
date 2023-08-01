import os

from flask import Blueprint, render_template, url_for, redirect, request, current_app
from flask_login import current_user, login_required
from sqlalchemy import desc, func, Integer, and_, or_

from app import db
from app.evaluators import Evaluator
from app.releases import Release, Status
from app.releases.controller import convert_pdf_to_data_url
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
    if not current_user.is_authenticated:
        # If the user is not authenticated, show only the projects which are accepted or rejected
        # (their latest release is accepted or rejected)
        latest_release_subquery = db.session.query(Release.project, func.max(Release.created_at).label('latest_date')) \
            .group_by(Release.project) \
            .subquery()
        query = query.join(latest_release_subquery, and_(Release.project == latest_release_subquery.c.project,
                                                         Release.created_at == latest_release_subquery.c.latest_date)) \
            .filter(or_(Release.status == Status.ACCEPTED, Release.status == Status.REJECTED))
    projects = query.all()
    return render_template('project_list.html', projects=projects, tag=tag)


@project.route('/view/<project_id>', methods=['GET', 'POST'])
def view(project_id):
    proj = Project.query \
        .join(Author, Author.project == Project.id) \
        .join(ProjectTag, ProjectTag.project == Project.id) \
        .join(Tag, Tag.id == ProjectTag.tag) \
        .outerjoin(Evaluator, Evaluator.id == Project.evaluator_id) \
        .outerjoin(Release, Release.project == Project.id) \
        .filter(Project.id == project_id) \
        .order_by(
            desc(Release.created_at),
            desc(func.cast(func.split_part(Release.version, '.', 1), Integer)),
            desc(func.cast(func.split_part(Release.version, '.', 2), Integer)),
        ).first()
    if proj.releases:
        for document in proj.releases[-1].documents:
            pdf_path = os.path.join(current_app.config['UPLOAD_FOLDER'], str(project_id), document.path)
            document.image_data_url = convert_pdf_to_data_url(pdf_path)
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


@project.route('<project_id>/assign_evaluator/<evaluator_id>', methods=['GET'])
def assign_evaluator(project_id, evaluator_id):
    proj = Project.query.get(project_id)
    proj.evaluator_id = evaluator_id
    proj.save(db)
    return redirect(url_for('project.view', project_id=proj.id))
