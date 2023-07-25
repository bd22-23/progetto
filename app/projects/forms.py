from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, widgets, Field
from wtforms.validators import InputRequired
from wtforms.widgets import TextArea, Input

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class NewProjectForm(FlaskForm):
    title = StringField(
        'Titolo',
        validators=[InputRequired()]
    )
    abstract = StringField(
        'Abstract',
        widget=TextArea(),
        validators=[InputRequired()]
    )
    tags = MultiCheckboxField('Tags')
    submit = SubmitField('Crea')

    def __init__(self, tags):
        super().__init__()
        self.tags.choices = [(str(tag.id), tag.value) for tag in tags]


class EditProjectForm(FlaskForm):
    title = StringField(
        'Titolo',
        validators=[InputRequired()]
    )
    abstract = StringField(
        'Abstract',
        widget=TextArea(),
        validators=[InputRequired()]
    )
    tags = MultiCheckboxField('Tags')
    reset = SubmitField(
        'Annulla',
        render_kw={'class': 'mt-2 btn btn-sm btn-secondary js-editable-stop-edit-button', 'type': 'reset'}
    )
    submit = SubmitField('Salva',
        render_kw={'class': 'mt-2 btn btn-sm btn-primary'}
    )

    def __init__(self, tags, project):
        super().__init__()
        self.tags.choices = [(str(tag.id), tag.value) for tag in tags]
        self.title.default = project.title
        self.abstract.default = project.abstract
        self.tags.default = [str(tag.id) for tag in project.tags]
        self.process()
