from flask import url_for
from flask_table import Table, Col


class DeleteAccountCol(Col):
    def td_contents(self, item, attr_list):
        delete_url = url_for('auth.delete_user', user_id=item.id)
        return f'<a href="{delete_url}" class="btn btn-block btn-danger"><span class="bi bi-trash"></span></a>'.format(item.id)


class EvaluatorTable(Table):
    classes = ['table', 'table-hover', 'table-striped', 'table-dark']
    table_id = 'evaluator-table'
    id = Col('Id', show=False)
    name = Col('Nome')
    surname = Col('Cognome')
    email = Col('Email')
    delete = DeleteAccountCol('Elimina')

    def get_tr_attrs(self, item):
        return {'id': f'{item.id}', 'class': 'evaluator-row'}


class ResearcherTable(Table):
    classes = ['table', 'table-hover', 'table-striped', 'table-dark']
    table_id = 'researcher-table'
    id = Col('Id', show=False)
    name = Col('Nome')
    surname = Col('Cognome')
    email = Col('Email')
    delete = DeleteAccountCol('Elimina')

    def get_tr_attrs(self, item):
        return {'id': f'{item.id}', 'class': 'researcher-row'}


class Item(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description
