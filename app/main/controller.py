from flask import Blueprint, render_template
from app.auth import UserMV

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    print(UserMV.query.all())
    return render_template("index.html")
