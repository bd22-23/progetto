import os

from flask import Blueprint, render_template, request, redirect, url_for, current_app
from sqlalchemy import desc
from werkzeug.utils import secure_filename

from app import db
from app.releases import Release, Document
from app.releases.forms import ReleaseForm

release = Blueprint('release', __name__, url_prefix='/release', template_folder='templates')


@release.route('/<project_id>/list', methods=['GET', 'POST'])
def list(project_id):
    releases = Release.query\
        .join(Document, Document.release == Release.id)\
        .filter(Release.project == project_id)\
        .all()
    return render_template('release_list.html', releases=releases)


@release.route('/<project_id>/view/<release_id>', methods=['GET', 'POST'])
def view(project_id, release_id):
    rel = Release.query\
        .join(Document, Document.release == Release.id)\
        .filter(Release.project == project_id)\
        .filter(Release.id == release_id)\
        .first()
    return render_template('release_view.html', release=rel, project_id=project_id)


@release.route('/<project_id>/new', methods=['GET', 'POST'])
def new(project_id):
    last_release = Release.query\
        .filter(Release.project == project_id)\
        .order_by(desc(Release.created_at))\
        .first()
    form = ReleaseForm(last_release.version if last_release else None)
    if form.validate_on_submit():
        rel = Release(
            project=project_id,
            version=form.version.data,
            status=Status.WAITING
        ).save(db)
        for file in form.files.data:
            Document(
                path=file.filename,
                release=rel.id,
            ).save(db)
            file_filename = secure_filename(file.filename)
            file.save(os.path.join(
                current_app.config['UPLOAD_FOLDER'] + '/' + str(project_id),
                file_filename
            ))
        return redirect(url_for('release.list', project_id=project_id))
    return render_template('release_new.html', form=form)
