from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from membership import db
from membership.main.forms import ResetPasswordForm
from membership.main.utils import send_reset_email
from membership.models import User, Unit
from flask_login import current_user
from sqlalchemy import or_

main = Blueprint('main', __name__)

#this is for sending members to pages that don't use the dashboard layout e.g. business members
@main.context_processor
def inject_menu():

    # Fill in with your actual menu dictionary:
    dashboard_units = Unit.query.all()
<<<<<<< HEAD

    return dict(dashboard_units=dashboard_units)
=======
    logged_in_user = current_user
    
   
    return dict(dashboard_units=dashboard_units, loggedinuser = logged_in_user)
>>>>>>> clone-main-branch


@main.route("/")
@main.route("/business-members")
def business_members():
  members = User.query.filter_by(role="USER").filter(User.business_name!=None).filter(User._is_suspended==False).all()
  units = Unit.query.all()
<<<<<<< HEAD
=======
  
>>>>>>> clone-main-branch

  return render_template("business_member.html", members= members, units=units)

@main.route("/business-members/search", methods=["POST"])
def search_business_members():
  query = request.form.get("search_query", False)
  page = request.args.get('page', 1, type=int)
  results = User.query.filter_by(role="USER").filter(User.business_name!=None).filter(User._is_suspended==False).filter(or_(User.business_name.ilike(f'%{query}%'), User.business_phone.ilike(f'%{query}%'), User.business_email.ilike(f'%{query}%') ))
  result_count = results.count()
  members = results.paginate(page=page, per_page=10)

  return render_template("business_search_results.html", result_count=result_count, members=members, query=query, title=f"Search Results for {query}")


@main.route("/business_unit_members/<int:unit_id>")
def business_unit_members(unit_id):
  page = request.args.get('page', 1, type=int)
  unit = Unit.query.filter_by(id=unit_id)[0]
  unit_members = unit.unit_members
  print(unit_members)
  members = unit_members.filter(User.business_name!=None).filter(User._is_suspended==False)

  return render_template("business_unit_members.html", members=members, unit=unit)


@main.route("/business-profile")
def business_profile():
  # members = User.query.filter_by(role="USER").all()

  return render_template("business_profile.html")

@main.route("/member_page/<string:business_name>", endpoint='member_page')
def member_page(business_name):
  if business_name == "None":
    abort(404)

  try:
    member = User.query.filter_by(business_name=business_name.replace("_", " "))[0]
  except IndexError:
    abort(404)

<<<<<<< HEAD
  image_file = url_for('static', filename='profile_pics/' + member.image_file)
=======
  # image_file = url_for('static', filename='profile_pics/' + member.image_file)
  image_file = url_for('static', filename='profile_pics/' + member.business_photo)
>>>>>>> clone-main-branch
  
  return render_template("member_page.html", member=member, image_file=image_file)



@main.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
  if current_user.is_authenticated:
    if current_user.role == "ADMIN":
      return redirect(url_for('admins.home'))
    elif current_user.role == "USER":
      return redirect(url_for('members.member-home'))

  if request.method == "POST":
    email_input = request.form['email']
    user = User.query.filter_by(email=email_input).first()
<<<<<<< HEAD
    if user:
      send_reset_email(user)
      flash('An email has been sent with instructions to reset your password.', 'info')
      return redirect(url_for('members.member-home'))
=======

    
    if user:
      send_reset_email(user)
      flash('An email has been sent with instructions to reset your password.', 'info')
      if user.role == 'ADMIN': 
        return redirect(url_for('admins.admin_login'))
      else:
        return redirect(url_for('members.login'))
>>>>>>> clone-main-branch
    else:
      flash('There is no account with that email. You must register first.', 'info')
  return render_template('reset_request.html', title='Reset Password')


@main.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
  if current_user.is_authenticated:
    if current_user.role == "ADMIN":
      return redirect(url_for('admins.home'))
    elif current_user.role == "USER":
      return redirect(url_for('members.member-home'))
  user = User.verify_reset_token(token)
  if user is None:
    flash('That is an invalid or expired token', 'warning')
    return redirect(url_for('main.reset_request'))
  form = ResetPasswordForm()
  if form.validate_on_submit():
    user.password = form.password.data
    db.session.commit()
    flash('Your password has been updated! You are now able to log in', 'success')
    return redirect(url_for('members.member-home'))
  return render_template('reset_token.html', title='Reset Password', form=form)