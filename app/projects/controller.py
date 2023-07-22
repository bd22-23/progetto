from flask import Blueprint, render_template, url_for

from app.projects import Project
from app.projects.tables import ProjectTable

project = Blueprint('project', __name__, url_prefix='/project', template_folder='templates')


@project.route('/list', methods=['GET', 'POST'])
def project_list():
    projects = Project.query.all()
    table = ProjectTable(projects)
    return render_template('project_list.html', project_table=table)


@project.route('/view/<project_id>', methods=['GET', 'POST'])
def project_view(project_id):
    proj = Project.query.filter_by(id=project_id).first()
    return render_template('project_view.html', project=proj)
