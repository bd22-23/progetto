from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import InputRequired
from wtforms.widgets import TextArea


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
    authors = SelectMultipleField(
        'Autori',
        render_kw={'class': 'js-editable-authors select2-selection select2-selection--multiple'},
    )
    reset = SubmitField(
        'Annulla',
        render_kw={'class': 'mt-2 btn btn-sm btn-secondary js-editable-stop-edit-button', 'type': 'reset'}
    )
    submit = SubmitField(
        'Salva',
        render_kw={'class': 'mt-2 btn btn-sm btn-primary'}
    )

    def __init__(self, tags, project, users):
        super().__init__()
        self.tags.choices = [(str(tag.id), tag.value) for tag in tags]
        self.authors.choices = [(str(user.id), user.name + " " + user.surname) for user in users]
        if not self.validate_on_submit():
            self.title.data = project.title
            self.abstract.data = project.abstract
            self.tags.data = [str(tag.id) for tag in project.tags]
            self.authors.data = [str(author.id) for author in project.authors]
