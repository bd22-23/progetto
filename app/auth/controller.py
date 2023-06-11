from flask import Blueprint, redirect, url_for, render_template, request, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.auth.forms import LoginForm
from app.auth.models import User
from app.researchers.models import Researcher

auth = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')


# @auth.route('/registration', methods=['GET', 'POST'])
# def register():
#     """
#         Renders the register page just for the researchers.
#     """
#     # if current_user.is_authenticated:
#     # redirect to home page if user is already logged in
#     form = RegisterForm(request.form)
#     if form.validate_on_submit():
#         name = form.name.data
#         surname = form.surname.data
#         email = form.email.data
#         password = generate_password_hash(form.password.data)
#         pronouns = form.pronouns.data
#         affiliation = form.affiliation.data
#         researcher = Researcher(name, surname, email, password, pronouns, affiliation)
#         researcher.save()
#         # redirect to appropriate page
#     return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    # redirect to home page if user is already logged in
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user is not None:
            if check_password_hash(password, user.password):
                login_user(user)
                # redirect to appropriate page
            else:
                flash('Password errata!')
        else:
            flash('Account inesistente!')
    return render_template('login.html', form=form)


# @auth.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('auth.index'))
