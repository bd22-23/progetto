from flask import url_for
from flask_table import Table, Col


class ProjectsTable(Table):
    classes = ['table', 'table-dark']
    table_id = 'project_table'
    id = Col('Id', show=False)
    title = Col('Nome', th_html_attrs={'class': 'hide-header-text'})
    abstract = Col('Abstract', show=False)

    def get_tr_attrs(self, item):
        project = f'{url_for("project.view", project_id=item.id)}'
        return {'id': f'{item.id}', 'class': 'clickable-row', 'onclick': 'window.location.href="' + project + '"'}
