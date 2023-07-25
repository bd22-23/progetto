from flask import Blueprint, render_template, current_app, url_for

from app.documents import Document
from app.releases import Release

document = Blueprint('document', __name__, url_prefix='/document', template_folder='templates')


@document.route('/<document_id>/view', methods=['GET', 'POST'])
def view(document_id):
    doc = Document.query \
        .join(Release, Release.id == Document.release) \
        .filter(Document.id == document_id) \
        .first()
    doc.path = url_for('static', filename='uploads/' + str(doc.releases.project) + '/' + doc.path)
    return render_template('view.html', document=doc)
