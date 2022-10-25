from flask import flash, url_for, redirect, request
from functools import wraps
from flask_login import current_user


def user_role_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
      if current_user.is_authenticated:
        if current_user.role == "USER":
          return func(*args, **kwargs)
        else:
          flash("You must log in to access this page")
          return redirect(url_for('members.login', next=url_for(request.endpoint)))
      else:
        flash("You must log in to access this page")
        return redirect(url_for('members.login', next=url_for(request.endpoint)))
    return decorated_view
