from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.validators import Email


class EditProfileForm(FlaskForm):

    name = StringField(
        'Nome'
    )
    surname = StringField(
        'Cognome'
    )
    role = StringField(
        'Ruolo'
    )
    affiliation = StringField(
        'Affiliazione'
    )
    pronouns = StringField(
        'Pronomi'
    )
    email = StringField(
        'Email',
        validators=[Email("Inserisci un'email valida!")]
    )
    submit = SubmitField('Salva')
