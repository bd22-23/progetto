from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

from app.auth.models import User


# class RegisterForm(FlaskForm):
#     name = StringField('Nome', validators=[DataRequired()])
#     surname = StringField('Cognome', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     pronouns = StringField('Pronomi', validators=[DataRequired()])
#     affiliation = StringField('Affiliazione', validators=[DataRequired()])
#     submit = SubmitField('Registrati!')

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user is not None:
    #         raise ValidationError('Email già presente! Scegline un\'altra.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user is None:
    #         raise ValidationError('Non sei registrato!')