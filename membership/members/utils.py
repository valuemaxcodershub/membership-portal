from flask import abort
from functools import wraps
from flask_login import current_user

def user_role_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
      if current_user.is_authenticated:
        if not current_user.role == "USER":
            abort(403)
        return func(*args, **kwargs)
      else:
        abort(403)
    return decorated_view

