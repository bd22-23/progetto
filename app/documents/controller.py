import json

from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import current_user

from app import db
from app.documents import Document
from app.releases import Release, Status

document = Blueprint('document', __name__, url_prefix='/document', template_folder='templates')


@document.route('/<document_id>/view', methods=['GET', 'POST'])
def view(document_id):
    doc = Document.query \
        .join(Release, Release.id == Document.release_id) \
        .filter(Document.id == document_id) \
        .first()
    editable = current_user.type == 'evaluator' and doc.release.status == Status.WAITING
    doc.path = url_for('static', filename='uploads/' + str(doc.release.project) + '/' + doc.path)
    return render_template('document_view.html', document=doc, editable=editable)


@document.route('/<document_id>/edit', methods=['POST'])
def update(document_id):
    data = json.loads(request.data)
    Document.query.filter(Document.id == document_id)\
        .update({'annotations': data})
    db.session.commit()
    return redirect(url_for('document.view', document_id=document_id))
