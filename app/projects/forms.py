from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, widgets


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class NewProjectForm(FlaskForm):

    name = StringField(
        'Nome'
    )
    abstract = StringField(
        'Abstract'
    )

    tags = MultiCheckboxField(
        'Tags'
    )
    submit = SubmitField('Crea')

    def __init__(self, tags):
        super().__init__()
        self.tags.choices = [(str(tag.id), tag.name) for tag in tags]
