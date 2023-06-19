from mistune import html
from flask import Blueprint, render_template

projects = Blueprint('projects', __name__, url_prefix='/projects', template_folder='templates')


@projects.route('/index', methods=['GET', 'POST'])
def index():
    file = open('app/static/docs/1.md', 'r', newline='').read()
    return render_template('test.html', file=html(file))

