from flask import Blueprint, render_template, redirect, url_for, flash, request
from membership import db
from membership.members.forms import UserLoginForm
from membership.models import User
from flask_login import login_user, current_user, logout_user
from membership.members.utils import user_role_required
from membership.main.utils import save_picture

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

@members.route("/create-business-profile", methods=["GET", "POST"])
@user_role_required
def create_business_profile():
  member = current_user
  if member.has_filled_profile:
    return redirect(url_for("members.edit_business_profile"))

  if request.method == "POST":
    member.business_name = request.form['business-name']
    member.business_email = request.form['business-email']
    member.business_website = request.form['business-website']
    member.business_phone = request.form["business-phone"]
    member.business_about = request.form["business-about"]
    member.business_facebook = request.form["business-facebook"]
    member.business_twitter = request.form["business-twitter"]
    member.business_linkedin = request.form["business-linkedin"]
    member.business_whatsapp = request.form["business-whatsapp"]

    if request.files['business-photo'].filename != '':
      member.business_photo = save_picture(request.files['business-photo'])

    if request.files['image-1'].filename != '':
      member.business_product_image_1 =  save_picture(request.files['image-1'])
    
    if request.files['image-2'].filename != '':
      member.business_product_image_2 =  save_picture(request.files['image-2'])
    
    if request.files['image-3'].filename != '':
      member.business_product_image_3 =  save_picture(request.files['image-3'])
    
    if request.files['image-4'].filename != '':
      member.business_product_image_4 =  save_picture(request.files['image-4'])
    
    if request.files['image-5'].filename != '':
      member.business_product_image_5 =  save_picture(request.files['image-5'])
    
    if request.files['image-6'].filename != '':
      member.business_product_image_6 =  save_picture(request.files['image-6'])

    member.has_filled_profile = True

    db.session.add(member)
    db.session.commit()

    return redirect(url_for('members.member_home'))




@members.route("/edit-business-profile", methods=["GET", "POST"])
@user_role_required
def edit_business_profile():
  member = current_user

  if request.method == "POST":
    member.business_name = request.form['business-name']
    member.business_email = request.form['business-email']
    member.business_website = request.form['business-website']
    member.business_phone = request.form["business-phone"]
    member.business_about = request.form["business-about"]
    member.business_facebook = request.form["business-facebook"]
    member.business_twitter = request.form["business-twitter"]
    member.business_linkedin = request.form["business-linkedin"]
    member.business_whatsapp = request.form["business-whatsapp"]

    if request.files['business-photo'].filename != '':
      member.business_photo = save_picture(request.files['business-photo'])

    if request.files['image-1'].filename != '':
      member.business_product_image_1 =  save_picture(request.files['image-1'])
    
    if request.files['image-2'].filename != '':
      member.business_product_image_2 =  save_picture(request.files['image-2'])
    
    if request.files['image-3'].filename != '':
      member.business_product_image_3 =  save_picture(request.files['image-3'])
    
    if request.files['image-4'].filename != '':
      member.business_product_image_4 =  save_picture(request.files['image-4'])
    
    if request.files['image-5'].filename != '':
      member.business_product_image_5 =  save_picture(request.files['image-5'])
    
    if request.files['image-6'].filename != '':
      member.business_product_image_6 =  save_picture(request.files['image-6'])

    db.session.add(member)
    db.session.commit()

    return redirect(url_for('members.member_home'))




  return render_template("business-profile-form.html", member=member)