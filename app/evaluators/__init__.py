from flask import abort
from functools import wraps
from flask_login import current_user
from app.evaluators.models import Evaluator


def evaluator_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.type != 'evaluator':
            abort(403)
        return func(*args, **kwargs)
    return wrapper
