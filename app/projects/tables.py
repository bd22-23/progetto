from flask import url_for
from flask_table import Table, Col


class ProjectTable(Table):
    classes = ['table', 'table-hover', 'table-striped', 'table-dark']
    table_id = 'project_table'
    id = Col('Id', show=False)
    name = Col('Nome', th_html_attrs={'class': 'hide-header-text'})
    abstract = Col('Abstract', show=False)

    def get_tr_attrs(self, item):
        project = f'{url_for("project.project_view", project_id=item.id)}'
        return {'id': f'{item.id}', 'class': 'clickable-row', 'onclick': 'window.location.href="' + project + '"'}