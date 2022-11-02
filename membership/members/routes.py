from flask import Blueprint, render_template, redirect, url_for, flash, request
from membership import db
from datetime import datetime
from membership.members.forms import UserLoginForm, CreateProfileForm, UserAccountForm
from membership.models import User, Unit, Message
from flask_login import login_user, current_user, logout_user
from membership.members.utils import user_role_required
from membership.main.utils import save_picture
from membership.admins.utils import add_member

members = Blueprint('members', __name__)

# @members.context_processor
# def inject_menu():

#     this_member = current_user

#     return this_member

@members.route('/dues', methods=['GET', 'POST'])
@user_role_required
def my_dues():
  
  return render_template("member_construction.html")

@members.route('/transaction-history', methods=['GET', 'POST'])
@user_role_required
def transaction_history():

  return render_template("member_construction.html")


@members.route("/member-home", methods=["GET", "POST"])
def member_home():
  if current_user.is_authenticated:
    if current_user.role == "ADMIN":
      return redirect(url_for("members.login"))

  return "Member Homepage"


@members.route("/member-dashboard", methods=["GET", "POST"])
@user_role_required
def dashboard():
  member = current_user

  return render_template("member_index.html", member=member)

@members.route("/messages", methods=["GET"])
@user_role_required
def messages():
  current_user.last_message_read_time = datetime.utcnow()
  db.session.commit()
  member = current_user

  messages = member.messages_received

  for unit in member.units:
    messages.extend(unit.messages_received)

  messages = messages.order_by(Message.timestamp.desc()).all()

  return render_template('messages.html', messages=messages, member=member)


@members.route("/login", methods=["GET", "POST"])
def login():
  if current_user.is_authenticated:
      if current_user.role == "USER":
        return redirect(url_for('members.dashboard'))

  form = UserLoginForm()


  if request.method == "POST":
    phone_input = request.form['phone']
    password_input = request.form['password']
    remember = form.remember.data
    user = User.query.filter_by(phone=phone_input).first()
    if user and user.password == password_input:
      login_user(user, remember=remember)
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('members.dashboard'))
    else:
      flash('Login Unsuccessful. Please check Phone number and password', 'danger')
    
  return render_template("user_login.html", title="Login", form=form)


@members.route("/account", methods=["GET", "POST"]) 
@user_role_required
def user_account():
  form = UserAccountForm()

  member = current_user
  form.current_member = current_user

  if form.validate_on_submit():
    if form.picture.data:
      picture_file = save_picture(form.picture.data)
      member.image_file = picture_file

    member.email = form.email.data
    member.phone = form.phone.data
    member.password = form.password.data
    
    db.session.add(member)
    db.session.commit()
    flash("Account successfuly modified", "success")
    return(redirect(url_for("members.dashboard")))
  elif request.method == 'GET':
    form.email.data = member.email
    form.phone.data = member.phone
    form.password.data = member.password

  image_file = url_for('static', filename='profile_pics/' + member.image_file)
  return render_template('user_account.html', member=member, form=form, image_file=image_file)


@members.route("/user-logout")
def user_logout():
    logout_user()
    return redirect(url_for('members.login'))

@members.route("/edit-business-profile", methods=["GET", "POST"])
@user_role_required
def edit_business_profile():
  member = current_user
  units = Unit.query.all()
  form = CreateProfileForm()

  if request.method == "GET":
    if member.business_name:
      print(member.business_services)
      form.business_name.data = member.business_name
      form.business_email.data = member.business_email
      form.business_website.data = member.business_website
      form.business_phone.data = member.business_phone 
      form.business_about.data = member.business_about  
      form.business_facebook.data = member.business_facebook
      form.business_twitter.data = member.business_twitter 
      form.business_linkedin.data = member.business_linkedin
      form.business_whatsapp.data = member.business_whatsapp
      form.business_address.data = member.business_address 
      form.business_services.data = member.business_services

  if form.validate_on_submit():
    member.business_name = form.business_name.data
    member.business_email = form.business_email.data
    member.business_website = form.business_website.data
    member.business_phone = form.business_phone.data
    member.business_about = form.business_about.data
    member.business_facebook = form.business_facebook.data
    member.business_twitter = form.business_twitter.data
    member.business_linkedin = form.business_linkedin.data
    member.business_whatsapp = form.business_whatsapp.data
    member.business_address = form.business_address.data
    member.business_services = form.business_services.data
    

    #save picture if it exists
    if form.business_photo.data:
      member.business_photo = save_picture(form.business_photo.data)
    if form.business_product_image_1.data:
      member.business_product_image_1 = save_picture(form.business_product_image_1.data)
    if form.business_product_image_2.data:
      member.business_product_image_2 = save_picture(form.business_product_image_2.data)
    if form.business_product_image_3.data:
      member.business_product_image_3 = save_picture(form.business_product_image_3.data)
    if form.business_product_image_4.data:
      member.business_product_image_4 = save_picture(form.business_product_image_4.data)
    if form.business_product_image_5.data:
      member.business_product_image_5 = save_picture(form.business_product_image_5.data)
    if form.business_product_image_6.data:
      member.business_product_image_6 = save_picture(form.business_product_image_6.data)

    selected_units = request.form.getlist('mymultiselect')

    add_member(member, selected_units=selected_units)

    return redirect(url_for('members.dashboard'))

  return render_template("business-profile-form.html", member=member, units=units, form=form)




# @members.route("/edit-business-profile", methods=["GET", "POST"])
# @user_role_required
# def edit_business_profile():
#   member = current_user
#   units = Unit.query.all()

#   if request.method == "POST":
#     member.business_name = request.form['business-name']
#     member.business_email = request.form['business-email']
#     member.business_website = request.form['business-website']
#     member.business_phone = request.form["business-phone"]
#     member.business_about = request.form["business-about"]
#     member.business_facebook = request.form["business-facebook"]
#     member.business_twitter = request.form["business-twitter"]
#     member.business_linkedin = request.form["business-linkedin"]
#     member.business_whatsapp = request.form["business-whatsapp"]

#     if request.files['business-photo'].filename != '':
#       member.business_photo = save_picture(request.files['business-photo'])

#     if request.files['image-1'].filename != '':
#       member.business_product_image_1 =  save_picture(request.files['image-1'])
    
#     if request.files['image-2'].filename != '':
#       member.business_product_image_2 =  save_picture(request.files['image-2'])
    
#     if request.files['image-3'].filename != '':
#       member.business_product_image_3 =  save_picture(request.files['image-3'])
    
#     if request.files['image-4'].filename != '':
#       member.business_product_image_4 =  save_picture(request.files['image-4'])
    
#     if request.files['image-5'].filename != '':
#       member.business_product_image_5 =  save_picture(request.files['image-5'])
    
#     if request.files['image-6'].filename != '':
#       member.business_product_image_6 =  save_picture(request.files['image-6'])

#     selected_units = request.form.getlist('mymultiselect')

#     add_member(member, selected_units=selected_units)

#     return redirect(url_for('members.member_home'))




#   return render_template("business-profile-form.html", member=member, units=units)