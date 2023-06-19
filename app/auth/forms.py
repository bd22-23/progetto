from flask_wtf import FlaskForm

from werkzeug.security import check_password_hash

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

from app.auth import User


class RegisterForm(FlaskForm):
    name = StringField(
        'Nome',
        validators=[DataRequired("Il nome è obbligatorio!")],
        render_kw={'placeholder': 'Mario'}
    )
    surname = StringField(
        'Cognome',
        validators=[DataRequired("Il cognome è obbligatorio!")],
        render_kw={'placeholder': 'Rossi'}
    )
    email = StringField(
        'Email',
        validators=[DataRequired("L'email è obbligatoria!"), Email("Inserisci un'email valida!")],
        render_kw={'placeholder': 'mariorossi@gmail.com'}
    )
    role = StringField(
        'Ruolo',
        render_kw={'placeholder': 'Ricercatore'}
    )
    password = PasswordField('Password', validators=[DataRequired("La password è obbligatoria!")])
    pronouns = StringField(
        'Pronomi',
        render_kw={'placeholder': 'he/him'}
    )
    affiliation = StringField(
        'Affiliazione', validators=[DataRequired("L'affiliazione è obbligatoria!")],
        render_kw={'placeholder': 'Università Ca\' Foscari di Venezia'}
    )
    submit = SubmitField('Registrati!')

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user is not None:
            self.form_errors.append('Email già registrata!')
            return False
        return True


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired("Inserisci un'email!"), Email("Inserisci un'email valida!")])
    password = PasswordField('Password', validators=[DataRequired("Inserisci una password!")])
    submit = SubmitField('Accedi')

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            self.form_errors.append('Email o password errati!')
            return False
        if not check_password_hash(user.password, self.password.data):
            self.form_errors.append('Email o password errati!')
            return False
        return True
