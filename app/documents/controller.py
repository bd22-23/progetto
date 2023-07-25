import json

from flask import Blueprint, render_template, current_app, url_for, request, redirect
from flask_login import current_user

from app import db
from app.documents import Document
from app.releases import Release

document = Blueprint('document', __name__, url_prefix='/document', template_folder='templates')


@document.route('/<document_id>/view', methods=['GET', 'POST'])
def view(document_id):
    editable = current_user.type == 'evaluator'
    doc = Document.query \
        .join(Release, Release.id == Document.release) \
        .filter(Document.id == document_id) \
        .first()
    doc.path = url_for('static', filename='uploads/' + str(doc.releases.project) + '/' + doc.path)
    return render_template('view.html', document=doc, editable=editable)


@document.route('/<document_id>/edit', methods=['POST'])
def update(document_id):
    data = json.loads(request.data)
    print(data)
    Document.query.filter(Document.id == document_id)\
        .update({'annotations': data})
    db.session.commit()
    return redirect(url_for('document.view', document_id=document_id))
