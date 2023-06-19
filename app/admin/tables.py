from flask_table import Table, Col


class ItemTable(Table):
    classes = ['table', 'table-hover', 'table-striped', 'table-bordered']
    id = Col('Id', show=False)
    name = Col('Nome')
    surname = Col('Cognome')
    email = Col('Email')
    bio = Col('Bio')
    pronouns = Col('Pronomi')
    grade = Col('Grado')


# Get some objects
class Item(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description