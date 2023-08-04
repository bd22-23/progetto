from flask import Blueprint, redirect, url_for, render_template, request, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash
from app import get_db_connection
from app.admin import admin_only
from app.auth import User
from app.auth.forms import LoginForm, RegisterForm
from app.researchers import Researcher

auth = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    db = get_db_connection()
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
            role=form.role.data,
            affiliation=form.affiliation.data
        ).save(db)
        login_user(user)
        return redirect(url_for('main.index'))
    else:
        for error in form.form_errors:
            flash(error, category='danger')
    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    db = get_db_connection()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.query(User).filter_by(email=form.email.data).first()
        if user is not None:
            login_user(user)
            current_user.id = user.id
            match user.type:
                case 'admin':
                    return redirect(url_for('main.index', profile_id=user.id))
                case 'evaluator':
                    return redirect(url_for('evaluator.profile', profile_id=user.id))
                case 'researcher':
                    return redirect(url_for('researcher.profile', profile_id=user.id))
    else:
        for error in form.form_errors:
            flash(error, category='danger')
    return render_template('login.html', form=form)


@auth.route('/delete/<user_id>')
@login_required
@admin_only
def delete_user(user_id):
    db = get_db_connection()
    user = db.query(User).filter_by(id=user_id).first()
    user.delete(db)
    return redirect(url_for('main.index'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
