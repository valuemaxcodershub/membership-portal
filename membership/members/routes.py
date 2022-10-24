from flask import Blueprint, render_template, redirect, url_for, flash, request
from membership.members.forms import UserLoginForm
from membership.models import User
from flask_login import login_user, current_user, logout_user
from membership.members.utils import user_role_required

members = Blueprint('members', __name__)


@members.route("/member-home", methods=["GET", "POST"])
def member_home():
  if current_user.is_authenticated:
    if current_user.role == "ADMIN":
      return redirect(url_for("members.login"))

  return "Member Homepage"


@members.route("/login", methods=["GET", "POST"])
def login():
  if current_user.is_authenticated:
      if current_user.role == "USER":
        return redirect(url_for('members.member_home'))

  form = UserLoginForm()


  if request.method == "POST":
    phone_input = request.form['phone']
    password_input = request.form['password']
    remember = form.remember.data
    user = User.query.filter_by(phone=phone_input).first()
    if user and user.password == password_input:
      login_user(user, remember=remember)
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('members.user_account'))
    else:
      flash('Login Unsuccessful. Please check Phone number and password', 'danger')
    
  return render_template("user_login.html", title="Login", form=form)


@members.route("/account") 
@user_role_required
def user_account():
    return render_template("user_account.html")

@members.route("/user-logout")
def user_logout():
    logout_user()
    return redirect(url_for('members.login'))

@members.route("/edit-business-profile")
@user_role_required
def edit_business_profile():
  members = User.query.filter_by(role="USER").all()
  if request.method == "POST":
    member.business_name = request.form['business-name']
    member.business_photo = request.form['business-photo']
    member.business_email = request.form['business-email']
    member.business_website = request.form['business-website']
    member.business_phone = request.form["business-phone"]
    member.business_about = request.form["business-about"]
    member.business_services = request.form["business-services"]
    member.business_facebook = request.form["business-facebook"]
    member.business_twitter = request.form["business-twitter"]
    member.business_linkedin = request.form["business-linkedin"]
    member.business_whatsapp = request.form["business-whatsapp"]

    image_str_list = []
    images = request.files.getlist('business-p-images')
    
    for image in images:
      if image:
        picture_file = save_picture(image)
        image_str_list.append(picture_file)
    
    member.business_images =  image_str_list


  return render_template("business-profile-form.html")