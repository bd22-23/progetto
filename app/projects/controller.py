import os

from flask import Blueprint, render_template, url_for, redirect, request, current_app, abort
from flask_login import current_user, login_required
from sqlalchemy import desc, func, Integer, and_, or_

from app import get_db_connection
from app.evaluators import Evaluator
from app.releases import Release, Status
from app.releases.controller import convert_pdf_to_data_url
from app.researchers import Author, Researcher, researcher_only
from app.projects import Project, ProjectTag, Tag
from app.projects.forms import NewProjectForm, EditProjectForm

project = Blueprint('project', __name__, url_prefix='/project', template_folder='templates')


@project.route('/list', methods=['GET', 'POST'])
def list():
    db = get_db_connection()
    tag = request.args.get('tag')
    query = db.query(Project) \
        .join(Researcher, Project.researchers) \
        .outerjoin(Tag, Project.tags) \
        .outerjoin(Release, Release.project_id == Project.id) \
        .filter(ProjectTag.project_id == Project.id)
    if tag:
        query = query.filter(Tag.value == tag)
    if not current_user.is_authenticated:
        # If the user is not authenticated, show only the projects which are accepted or rejected
        # (their latest release is accepted or rejected)
        latest_release_subquery = db.query(Release.project_id, func.max(Release.created_at).label('latest_date')) \
            .group_by(Release.project_id) \
            .subquery()
        query = query.join(latest_release_subquery, and_(Release.project_id == latest_release_subquery.c.project_id,
                                                         Release.created_at == latest_release_subquery.c.latest_date)) \
            .filter(or_(Release.status == Status.ACCEPTED, Release.status == Status.REJECTED))
    projects = query.all()
    return render_template('project_list.html', projects=projects, tag=tag)


@project.route('/view/<project_id>', methods=['GET', 'POST'])
def view(project_id):
    db = get_db_connection()
    proj = db.query(Project) \
        .join(Researcher, Project.researchers) \
        .outerjoin(Tag, Project.tags) \
        .outerjoin(Evaluator, Evaluator.id == Project.evaluator_id) \
        .outerjoin(Release, Release.project_id == Project.id) \
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
    tags = db.query(Tag).all()
    users = db.query(Researcher).all()
    form = EditProjectForm(tags, proj, users)
    if form.validate_on_submit():
        if current_user.id not in [researcher.id for researcher in proj.researchers]:
            return abort(403)
        proj.title = form.title.data
        proj.abstract = form.abstract.data
        proj.save(db)
        db.query(ProjectTag).filter_by(project_id=proj.id).delete()
        for tag in form.tags.data:
            ProjectTag(proj.id, tag).save(db)
        db.query(Author).filter_by(project_id=proj.id).delete()
        for author in form.authors.data:
            Author(proj.id, author).save(db)
        return redirect(url_for('project.view', project_id=proj.id))
    return render_template('project_view.html', project=proj, tags=tags, form=form)


@project.route('/new', methods=['GET', 'POST'])
@login_required
@researcher_only
def new():
    db = get_db_connection()
    tags = db.query(Tag).all()
    form = NewProjectForm(tags)
    if form.validate_on_submit():
        proj = Project(
            title=form.title.data,
            abstract=form.abstract.data
        ).save(db)
        Author(
            project_id=proj.id,
            researcher_id=current_user.id
        ).save(db)
        os.makedirs(os.path.dirname(current_app.config['UPLOAD_FOLDER'] + '/' + str(proj.id) + '/'), exist_ok=True)
        for tag in form.tags.data:
            ProjectTag(proj.id, tag).save(db)
        return redirect(url_for('project.view', project_id=proj.id))
    return render_template('project_new.html', form=form)


@project.route('<project_id>/assign_evaluator/<evaluator_id>', methods=['GET'])
def assign_evaluator(project_id, evaluator_id):
    db = get_db_connection()
    proj = db.query(Project).get(project_id)
    proj.evaluator_id = evaluator_id
    proj.save(db)
    return redirect(url_for('project.view', project_id=proj.id))


@project.route('/delete/<project_id>', methods=['GET', 'POST'])
@login_required
@researcher_only
def delete(project_id):
    db = get_db_connection()
    proj = db.query(Project).filter_by(id=project_id).first()
    if current_user.id not in [researcher.id for researcher in proj.researchers]:
        return abort(403)
    proj.delete(db)
    return redirect(url_for('project.list'))
