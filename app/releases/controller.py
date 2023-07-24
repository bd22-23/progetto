from flask import Blueprint, render_template

from app.releases import Release

release = Blueprint('release', __name__, url_prefix='/release', template_folder='templates')


@release.route('/<project_id>:int/list', methods=['GET', 'POST'])
def list(project_id):
    releases = Release.query.filter(Release.project == project_id).all()
    return render_template('release_list.html', releases=releases)


@release.route('/<project_id>:int/new', methods=['GET', 'POST'])
def new(project_id):
    return render_template('release_new.html', project_id=project_id)
