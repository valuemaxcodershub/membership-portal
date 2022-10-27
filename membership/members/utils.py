from flask import flash, url_for, redirect, request
from functools import wraps
from flask_login import current_user, logout_user


def user_role_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
      if current_user.is_authenticated:
        if current_user.role == "USER":
          if current_user.business_name == None and request.endpoint != 'members.edit_business_profile' and request.method!="POST":
            flash("You must first complete this form before you can proceed")
            return redirect(url_for('members.edit_business_profile'))

          return func(*args, **kwargs)
        else:
          flash("You must log in to access this page", "info")
          return redirect(url_for('members.login', next=url_for(request.endpoint)))
      else:
        flash("You must log in to access this page", "info")
        return redirect(url_for('members.login', next=url_for(request.endpoint)))
    return decorated_view
