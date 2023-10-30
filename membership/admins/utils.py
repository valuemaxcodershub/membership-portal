from flask import abort, redirect, url_for, request, flash
from membership import login_manager
from membership import db
from membership.models import User, Unit
from flask_login import current_user
import secrets
import csv
from functools import wraps




class DataStore():
    a = None


def admin_role_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
      if current_user.is_authenticated:
        if current_user.role == "ADMIN":
          return func(*args, **kwargs)
        else:
          flash("You must log in to access this page", "info")
          return redirect(url_for('admins.admin_login', next=url_for(request.endpoint)))
      else:
          flash("You must log in to access this page", "info")
          return redirect(url_for('admins.admin_login', next=url_for(request.endpoint)))
    return decorated_view

def super_admin_role_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
      if current_user.is_authenticated:
        if current_user.role == "USER":
          flash("You must log in to access this page", "info")
          return redirect(url_for('admins.admin_login', next=url_for(request.endpoint)))
        elif not current_user.is_superadmin:
            abort(403)
        return func(*args, **kwargs)
      else:
        return redirect(url_for('admins.admin_login', next=url_for(request.endpoint)))

    return decorated_view
    

def parse_csv(csv_file):
  with open(csv_file) as csv_file:
    csv_reader = csv.DictReader(csv_file)

    #compulsory items
    params = ["phone"]

    for row in csv_reader:
      user = User()
      #Set the values of the items that exist in class
      for key, value in row.items():
        if key in params:
          print(f"{key} =  {value}")
          setattr(user, key, value)

      # assign units
      if "unit_ids" in params:
        unit_ids = row["unit_ids"].split("-")
        print(unit_ids)
        if unit_ids != ['']:
          for unit_id in unit_ids:
            unit = Unit.query.get(int(unit_id))
            if unit:
              user.units.append(unit)


      # user.password = secrets.token_urlsafe(8)
      db.session.add(user)



def add_member(user, selected_units=None):

# checking whether the passed in user's phone number exists or not and creating new instance if not exists.
  if User.query.filter_by(phone = user).first():
    member = User.query.filter_by(phone= user).first()
  else:
    member = User(phone = user)

  db.session.add(member)
  db.session.commit()
  
  # checking whether units have been selected when a member's account is being updated
  if selected_units:
    inputted_units = []
    for unit_name in selected_units:
      unit = Unit.query.filter_by(name=unit_name).all()[0]
      inputted_units.append(unit)
    
    member.units = inputted_units
    db.session.commit()
    