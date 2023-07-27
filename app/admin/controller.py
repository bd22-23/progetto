from flask import Blueprint, render_template
from flask_login import login_required
from app.role_required_decorator import role_required

from app.admin.tables import EvaluatorTable, ResearcherTable

from app.evaluators import Evaluator
from app.researchers import Researcher

admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')


@role_required('admin')
@admin.route('/researchers')
@login_required
def researchers():
    researchers = Researcher.query.with_entities(
        Researcher.id, Researcher.name, Researcher.surname, Researcher.email
    ).all()

    researcher_table = ResearcherTable(researchers)

    return render_template('researchers.html', researcher_table=researcher_table)


@admin.route('/evaluators')
@login_required
def evaluators():
    evals = Evaluator.query.with_entities(
        Evaluator.id, Evaluator.name, Evaluator.surname, Evaluator.email
    ).all()

    evaluator_table = EvaluatorTable(evals)

    return render_template('evaluators.html', evaluator_table=evaluator_table)

