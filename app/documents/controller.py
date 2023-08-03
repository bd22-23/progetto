import json

from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import current_user

from app import get_db_connection
from app.documents import Document
from app.projects import Project
from app.releases import Release, Status

document = Blueprint('document', __name__, url_prefix='/document', template_folder='templates')


@document.route('/<document_id>/view', methods=['GET', 'POST'])
def view(document_id):
    db = get_db_connection()
    doc = db.query(Document) \
        .join(Release, Release.id == Document.release_id) \
        .join(Project, Project.id == Release.project_id) \
        .filter(Document.id == document_id) \
        .first()

    editable = current_user.is_authenticated \
               and current_user.type == 'evaluator' \
               and doc.release.status == Status.WAITING \
               and doc.release.project.evaluator_id == current_user.id
    doc.path = url_for('static', filename='uploads/' + str(doc.release.project_id) + '/' + doc.path)
    return render_template('document_view.html', document=doc, editable=editable)


@document.route('/<document_id>/edit', methods=['POST'])
def update(document_id):
    db = get_db_connection()
    data = json.loads(request.data)
    db.query(Document).filter(Document.id == document_id) \
        .update({'annotations': data})
    db.session.commit()
    return redirect(url_for('document.view', document_id=document_id))
