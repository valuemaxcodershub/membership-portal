from flask import abort, redirect, url_for, request
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
        if not current_user.role == "ADMIN":
            abort(403)
        return func(*args, **kwargs)
      else:
        return redirect(url_for('admins.admin_login', next=url_for(request.endpoint)))
    return decorated_view

def super_admin_role_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
      if current_user.is_authenticated:
        if not current_user.is_superadmin:
            abort(403)
        return func(*args, **kwargs)
      else:
        return redirect(url_for('admins.admin_login', next=url_for(request.endpoint)))
    return decorated_view
    

def parse_csv(csv_file):
  with open(csv_file) as csv_file:
    csv_reader = csv.DictReader(csv_file)

    #compulsory items
    params = ["username", "phone", "email", "unit_ids", "image_file", "current_salary", "occupation", "experience", "date_of_birth", "home_address", "work_address"]



    for row in csv_reader:
      user = User()
      #Set the values of the items that exist in class
      for key, value in row.items():
        if key in params:
          print(f"{key} =  {value}")
          setattr(user, key, value)
         
            

      # assign units
      unit_ids = row["unit_ids"].split("-")
      print(unit_ids)
      if unit_ids != ['']:
        for unit_id in unit_ids:
          unit = Unit.query.get(int(unit_id))
          if unit:
            user.units.append(unit)


      user.password = secrets.token_urlsafe(8)
      db.session.add(user)
