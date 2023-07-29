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


class EditProfileForm(FlaskForm):

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
                self.bio.data = user.bio
                self.email.data = user.email
                self.pronouns.data = user.pronouns