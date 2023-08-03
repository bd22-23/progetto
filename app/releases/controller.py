import os
import base64

from flask import Blueprint, render_template, request, redirect, url_for, current_app
from sqlalchemy import desc
from werkzeug.utils import secure_filename

from app import get_db_connection
from app.releases import Release
from app.releases import ReleaseForm
from app.releases import Status
from app.documents import Document

release = Blueprint('release', __name__, url_prefix='/release', template_folder='templates')


def convert_pdf_to_data_url(pdf_path):
    with open(pdf_path, "rb") as file:
        pdf_data = file.read()
        encoded_pdf = base64.b64encode(pdf_data).decode("utf-8")
        data_url = f"data:application/pdf;base64,{encoded_pdf}"
        return data_url


@release.route('/<project_id>/view/<release_id>', methods=['GET', 'POST'])
def view(project_id, release_id):
    db = get_db_connection()
    rel = db.query(Release)\
        .join(Document, Document.release_id == Release.id)\
        .filter(Release.project_id == project_id)\
        .filter(Release.id == release_id)\
        .first()
    for document in rel.documents:
        pdf_path = os.path.join(current_app.config['UPLOAD_FOLDER'], str(project_id), document.path)
        document.image_data_url = convert_pdf_to_data_url(pdf_path)
    return render_template('release_view.html', release=rel, project_id=project_id)


@release.route('/<project_id>/update/<release_id>', methods=['POST'])
def update(project_id, release_id):
    db = get_db_connection()
    stat = Status(request.form['status'])
    db.query(Release).filter(Release.id == release_id)\
        .update({'status': stat})
    db.session.commit()
    return redirect(url_for('release.view', project_id=project_id, release_id=release_id))


@release.route('/<project_id>/new', methods=['GET', 'POST'])
def new(project_id):
    db = get_db_connection()
    last_release = db.query(Release)\
        .filter(Release.project_id == project_id)\
        .order_by(desc(Release.created_at))\
        .first()
    form = ReleaseForm(last_release.version if last_release else None)
    if form.validate_on_submit():
        rel = Release(
            project_id=project_id,
            version=form.version.data,
            status=Status.WAITING
        ).save(db)
        # Create folder for project if it doesn't exist
        from pathlib import Path
        Path(current_app.config['UPLOAD_FOLDER'] + '/' + str(project_id))\
            .mkdir(parents=True, exist_ok=True)
        for file in form.files.data:
            file_filename = secure_filename(file.filename)
            Document(
                path=secure_filename(file.filename),
                release_id=rel.id,
            ).save(db)
            file.save(os.path.join(
                current_app.config['UPLOAD_FOLDER'] + '/' + str(project_id),
                file_filename
            ))
        return redirect(url_for('project.view', project_id=project_id))
    return render_template('release_new.html', form=form)
