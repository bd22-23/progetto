from flask import Blueprint, redirect, url_for, render_template
from flask_login import logout_user, login_required

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    return render_template("index.html")