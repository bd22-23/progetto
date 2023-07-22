from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Email


class NewProfileForm(FlaskForm):

    name = StringField(
        'Nome'
    )
    surname = StringField(
        'Cognome'
    )
    bio = StringField(
        'Bio'
    )
    pronouns = StringField(
        'Pronomi'
    )
    email = StringField(
        'Email',
        validators=[Email("Inserisci un'email valida!")]
    )
    password = PasswordField(
        'Password'
    )
    submit = SubmitField('Crea')
