from flask import abort
from functools import wraps
from flask_login import current_user
from app.researchers.models import Researcher, Author


def researcher_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.type != 'researcher':
            abort(403)
        return func(*args, **kwargs)
    return wrapper
