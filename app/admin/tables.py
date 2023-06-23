from flask_table import Table, Col


class EvaluatorTable(Table):
    classes = ['table', 'table-hover', 'table-striped']
    table_id = 'evaluator-table'
    id = Col('Id', show=False)
    name = Col('Nome')
    surname = Col('Cognome')
    email = Col('Email')

    def get_tr_attrs(self, item):
        return {'id': f'{item.id}', 'class': 'evaluator-row'}


class ResearcherTable(Table):
    classes = ['table', 'table-hover', 'table-striped']
    table_id = 'researcher-table'
    id = Col('Id', show=False)
    name = Col('Nome')
    surname = Col('Cognome')
    email = Col('Email')

    def get_tr_attrs(self, item):
        return {'id': f'{item.id}', 'class': 'evaluator-row'}


class Item(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description
