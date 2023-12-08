from flask import flash, url_for, redirect, request
from functools import wraps
from flask_login import current_user, logout_user
from membership.models import User


#this exists to allow only users login
def user_role_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
      if current_user.is_authenticated:
        if current_user.role == "USER":

          #suspended users can not log in
          if current_user._is_suspended:
            logout_user()
            flash("Your account has been suspended and you can therefore not log in", "danger")
            return redirect(url_for('members.login'))

          #logic for users to first fill their form before accessing other pages
          if current_user.business_name == None and request.endpoint != 'members.edit_business_profile' and request.method!="POST":

            if current_user.has_filled_profile and (current_user.update_is_approved == User.USER_UPDATE_PENDING ):
              flash("Your profile update is awaiting admin approval", category="info")
            elif current_user.has_filled_profile and current_user.update_is_approved == User.USER_UPDATE_DISAPPROVED:
              flash("Your profile update has been rejected by admin. Please, fill in valid details and try again.", category="warning")
            else:
              flash("You must first complete this form before you can proceed", category="warning")
              
            return redirect(url_for('members.edit_business_profile'))

          return func(*args, **kwargs)
        

        else:
          flash("You must log in to access this page", category="info")
          return redirect(url_for('members.login', next=url_for(request.endpoint)))
        
        
      else:
        flash("You must log in to access this page", category="info")
        return redirect(url_for('members.login', next=url_for(request.endpoint)))
    return decorated_view
