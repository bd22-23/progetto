from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import InputRequired


class EditResearcherForm(FlaskForm):
    name = StringField(
        'Nome',
        validators=[InputRequired()]
    )
    surname = StringField(
        'Cognome',
        validators=[InputRequired()]
    )
    role = StringField(
        'Ruolo',
        validators=[InputRequired()]
    )
    affiliation = StringField(
        'Affiliazione',
        validators=[InputRequired()]
    )
    email = EmailField(
        'Affiliazione',
        validators=[InputRequired()]
    )
    pronouns = StringField(
        'Pronomi'
    )
    reset = SubmitField(
        'Annulla',
        render_kw={'class': 'mt-2 btn btn-sm btn-secondary js-editable-stop-edit-button', 'type': 'reset'}
    )
    submit = SubmitField(
        'Salva',
        render_kw={'class': 'mt-2 btn btn-sm btn-primary'}
    )

    def __init__(self, user):
        super().__init__()
        if not self.validate_on_submit():
            self.name.data = user.name
            self.surname.data = user.surname
            self.role.data = user.role
            self.affiliation.data = user.affiliation
            self.email.data = user.email
            self.pronouns.data = user.pronouns
