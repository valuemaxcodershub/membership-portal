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

  member = User.query.get_or_404(user.id)
  if selected_units:
    inputted_units = []
    for unit_name in selected_units:
      unit = Unit.query.filter_by(name=unit_name).all()[0]
      inputted_units.append(unit)

    print('From the appended, we have: ', inputted_units)
    
    # member.units.delete_all()
    # db.session.remove()
    print('previous units: ', member.units.all())

    print('Trying to addit now.')
    member.units = inputted_units
    print('WoW!!!!!! Sucessfully done.....')
    # for unit in inputted_units:
    #   member.units.append(unit)

    #   print('Added to ::; ', member.units.all())

    # print('At the end:::: ', member.units.all())
  db.session.add(member)
  db.session.commit()
