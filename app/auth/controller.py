from flask import Blueprint, redirect, url_for, render_template, request, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.auth import UserMV
from app.auth.forms import LoginForm, RegisterForm
from app.researchers import Researcher

auth = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = Researcher(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            pronouns=form.pronouns.data,
            affiliation=form.affiliation.data
        ).save(db)
        login_user(user)
        redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = UserMV.query.filter_by(email=email).first()
        if user is None:
            flash('Email or password are wrong!', 'danger')
        elif not check_password_hash(password=password, pwhash=user.password):
            flash('Email or password are wrong!', 'danger')
        else:
            login_user(user)
            return redirect(url_for('main.index'))
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
