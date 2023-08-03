import os

from flask import Blueprint, render_template, url_for, redirect, request, current_app
from flask_login import current_user, login_required
from sqlalchemy import desc, func, Integer, and_, or_

from app import db
from app.evaluators import Evaluator
from app.releases import Release, Status
from app.releases.controller import convert_pdf_to_data_url
from app.researchers import Author, Researcher, researcher_only
from app.projects import Project, ProjectTag, Tag
from app.projects.forms import NewProjectForm, EditProjectForm

project = Blueprint('project', __name__, url_prefix='/project', template_folder='templates')


@project.route('/list', methods=['GET', 'POST'])
def list():
    with db.session(bind='appuser'):
        tag = request.args.get('tag')
        query = Project.query \
            .join(Author, Author.project == Project.id) \
            .join(ProjectTag, ProjectTag.project == Project.id) \
            .join(Tag, Tag.id == ProjectTag.tag) \
            .outerjoin(Release, Release.project_id == Project.id) \
            .filter(ProjectTag.project == Project.id)
        if tag:
            query = query.filter(Tag.value == tag)
        if not current_user.is_authenticated:
            # If the user is not authenticated, show only the projects which are accepted or rejected
            # (their latest release is accepted or rejected)
            latest_release_subquery = db.session.query(Release.project_id, func.max(Release.created_at).label('latest_date')) \
                .group_by(Release.project_id) \
                .subquery()
            query = query.join(latest_release_subquery, and_(Release.project_id == latest_release_subquery.c.project_id,
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


@project.route('/new', methods=['GET', 'POST'])
@login_required
@researcher_only
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

  
@project.route('/delete/<project_id>', methods=['GET', 'POST'])
@login_required
@researcher_only
def delete(project_id):
    proj = Project.query.filter_by(id=project_id).first()
    proj.delete(db)
    return redirect(url_for('project.list'))
