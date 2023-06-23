from flask import Blueprint, render_template

from app.admin.tables import EvaluatorTable, ResearcherTable

from app.evaluators import Evaluator
from app.researchers import Researcher

admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')


@admin.route('/')
def index():
    # fetch only id, name, surname, email
    evaluators = Evaluator.query.with_entities(Evaluator.id, Evaluator.name, Evaluator.surname, Evaluator.email).all()
    researchers = Researcher.query.with_entities(Researcher.id, Researcher.name, Researcher.surname, Researcher.email).all()

    evaluator_table = EvaluatorTable(evaluators)
    researcher_table = ResearcherTable(researchers)

    return render_template('admin-panel.html', evaluator_table=evaluator_table, researcher_table=researcher_table)
