from flask import Blueprint, render_template
from app.auth import User

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    print(User.query.all())
    return render_template("index.html")
