from flask import Blueprint, render_template

from app.admin.tables import ItemTable

from app.evaluators import Evaluator

admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')


@admin.route('/')
def index():
    items = Evaluator.query.all()
    table = ItemTable(items)
    return render_template('admin-panel.html', table=table)
