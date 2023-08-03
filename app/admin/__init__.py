from flask import abort
from functools import wraps
from flask_login import current_user
from app.admin.models import Admin


def admin_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.type != 'admin':
            abort(403)
        return func(*args, **kwargs)
    return wrapper
