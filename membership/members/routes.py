from flask import Blueprint, render_template, redirect, url_for, flash, request
import json
from membership import db
from datetime import datetime
from membership.members.forms import UserLoginForm, CreateProfileForm, UserAccountForm
from membership.models import User, Unit, Message, UserUpdate
from flask_login import login_user, current_user, logout_user
from membership.members.utils import user_role_required
from membership.main.utils import save_picture
from membership.admins.utils import add_member

members = Blueprint('members', __name__)

@members.context_processor
def inject_menu():

    this_member = current_user

    if this_member.is_authenticated:

      last_read_time = this_member.last_message_read_time or datetime(1900, 1, 1)

      print('Count of messages: ', Message.query.filter_by(member_recipient_id= this_member.id).filter(
          Message.timestamp > last_read_time).count())

    return dict(this_member = this_member, loggedinuser = current_user)

@members.route('/dues', methods=['GET', 'POST'])
@user_role_required
def my_dues():
  
  return render_template("member/member_construction.html")

@members.route('/transaction-history', methods=['GET', 'POST'])
@user_role_required
def transaction_history():

  return render_template("member/member_construction.html")


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

  return render_template("member/member_index.html", member=member)

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

    
    user = User.query.filter_by(business_phone=phone_input).first()
    if user and user.password == password_input:
      login_user(user, remember=remember)
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('members.dashboard'))
    else:
      flash('Login Unsuccessful. Please check Phone number and password', 'danger')
    
  return render_template("member/user_login.html", title="Login", form=form)


@members.route("/account", methods=["GET", "POST"]) 
@user_role_required
def user_account():
  form = UserAccountForm()

  member = current_user
  form.current_member = current_user

  if form.validate_on_submit():
    if form.picture.data:
      picture_file = save_picture(form.picture.data)
      member.business_photo = picture_file

    member.business_email = form.email.data
    member.business_phone = form.phone.data
    member.password = form.password.data
    
    db.session.add(member)
    db.session.commit()
    flash("Account successfuly modified", "success")
    return(redirect(url_for("members.dashboard")))
  
  elif request.method == 'GET':
    form.email.data = member.business_email
    form.phone.data = member.business_phone
    form.password.data = member.password


  image_file = url_for('static', filename='profile_pics/' + member.business_photo )
  return render_template('member/user_account.html', member=member, form=form, image_file=image_file)


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
      form.business_name.data = member.business_name
      form.business_email.data = member.business_email
      form.business_website.data = member.business_website
      form.business_phone.data = member.business_phone 
      form.business_about.data = member.business_about  
      form.business_photo.data = member.business_photo  
      form.business_facebook.data = member.business_facebook
      form.business_twitter.data = member.business_twitter 
      form.business_linkedin.data = member.business_linkedin
      form.business_whatsapp.data = member.business_whatsapp
      form.business_address.data = member.business_address 
      form.business_services.data = member.business_services
      form.date_of_birth.data = member.date_of_birth
      form.password.data = member.password

  if request.method == 'POST':
    if form.validate_on_submit():

      userd = {}
      
      if member.business_name != form.business_name.data:
        userd.update({'business_name': form.business_name.data})
      
      if member.business_email != form.business_email.data:
        userd.update({'business_email': form.business_email.data})
      if member.business_website != form.business_website.data:
        userd.update({'business_website': form.business_website.data})
      if member.business_phone != form.business_phone.data:
        userd.update({'business_phone': form.business_phone.data})
      if member.business_about != form.business_about.data:
        userd.update({'business_about': form.business_about.data})
      if member.business_facebook != form.business_facebook.data:
        userd.update({'business_facebook': form.business_facebook.data})
      if member.business_twitter != form.business_twitter.data:
        userd.update({'business_twitter': form.business_twitter.data})
      if member.business_linkedin != form.business_linkedin.data:
        userd.update({'business_linkedin': form.business_linkedin.data})
      if member.business_whatsapp != form.business_whatsapp.data:
        userd.update({'business_whatsapp': form.business_whatsapp.data})
      if member.business_address != form.business_address.data:
        userd.update({'business_address': form.business_address.data})
      if member.business_services != form.business_services.data:
        userd.update({'business_services': form.business_services.data })

      member.password = form.password.data
      member.update_is_approved = User.USER_UPDATE_PENDING
      member.has_filled_profile = True
      # member.date_of_birth = form.date_of_birth.data

      if form.business_photo.data:
        # member.business_photo = save_picture(form.business_photo.data)
        photo = save_picture(form.business_photo.data)
        userd.update({'business_photo': photo})
      
      
      if form.business_product_image_1.data:
        business_product_image_1 = save_picture(form.business_product_image_1.data)
        userd.update({'business_product_image_1': business_product_image_1})
      if form.business_product_image_2.data:
        business_product_image_2 = save_picture(form.business_product_image_2.data)
        userd.update({'business_product_image_2': business_product_image_2})
      if form.business_product_image_3.data:
        business_product_image_3 = save_picture(form.business_product_image_3.data)
        userd.update({'business_product_image_3': business_product_image_3})
      if form.business_product_image_4.data:
        business_product_image_4 = save_picture(form.business_product_image_4.data)
        userd.update({'business_product_image_4': business_product_image_4})
      if form.business_product_image_5.data:
        business_product_image_5 = save_picture(form.business_product_image_5.data)
        userd.update({'business_product_image_5': business_product_image_5})
      if form.business_product_image_6.data:
        business_product_image_6 = save_picture(form.business_product_image_6.data)
        userd.update({'business_product_image_6': business_product_image_6})

      selected_units = request.form.getlist('mymultiselect')
      userd.update({'selected_units': selected_units})

      user_data_json = json.dumps(userd)
     
      
      new_update_from_user = UserUpdate(userid = member.id, update=user_data_json)
      db.session.add(member)
      db.session.add(new_update_from_user)
      db.session.commit()

      # add_member(member.business_phone, selected_units=selected_units)

      return redirect(url_for('members.dashboard'))

    else:
      print('FORM ERROR: ', form.errors)
  return render_template("member/business-profile-form.html", member=member, units=units, form=form)
