from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import InputRequired
from wtforms.widgets import TextArea


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class NewProjectForm(FlaskForm):
    title = StringField('Titolo', validators=[InputRequired()])
    abstract = StringField('Abstract', widget=TextArea(), validators=[InputRequired()])
    tags = MultiCheckboxField('Tags')
    submit = SubmitField('Crea')

    def __init__(self, tags):
        super().__init__()
        self.tags.choices = [(str(tag.id), tag.name) for tag in tags]
