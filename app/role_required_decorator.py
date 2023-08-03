from functools import wraps
from flask import abort
from flask_login import current_user
import app


def role_required(required_role):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return app.login_manager.unauthorized()
            if not current_user.has_role(required_role):
                abort(403)  # Forbidden
            return func(*args, **kwargs)
        return decorated_function
    return decorator
