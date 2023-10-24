from flask import render_template, redirect, url_for, flash, request
import os
from PIL import Image
from membership import app, db, bcrypt, mail
from membership.forms import RegistrationForm, UserLoginForm, AdminLoginForm, UpdateMemberForm, RequestResetForm, ResetPasswordForm
from membership.models import User
from flask_login import login_user, current_user, logout_user, login_required
import secrets
from flask_mail import Message

#ALL ALL ALL#
@app.route("/")
@app.route("/home")
def home():
  return render_template("home.html")

@app.route("/account")
@login_required
def account():
  if current_user.role == "USER":
    return render_template("user_account.html")
  elif current_user.role == "ADMIN":
    return render_template("admin_account.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


# USER USER USER #
@app.route("/login", methods=["GET", "POST"])
def user_login():
  if current_user.is_authenticated:
      return redirect(url_for('home'))
  form = UserLoginForm()
  if form.validate_on_submit():
    
    user = User.query.filter_by(phone=form.phone.data).first()
    if user and user.password == form.password.data:
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('home'))
    else:
      flash('Login Unsuccessful. Please check email and password', 'danger')
    
  return render_template("user_login.html", title="Login", form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (2055, 2055)
    i = Image.open(form_picture)
    # i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



# ADMIN ADMIN ADMIN #
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
  if current_user.is_authenticated:
    if current_user.role == "ADMIN":
      return redirect(url_for('admin'))
    else:
      flash("You need to be an admin to view this page.")
      return redirect(url_for('home'))
    
  form = AdminLoginForm()
  
  if form.validate_on_submit():
    admin = User.query.filter_by(role="ADMIN").filter_by(email=form.email.data).first()
    if admin and admin.password == form.password.data:
      login_user(admin, remember=form.remember.data)
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('admin'))
    else:
      flash('Login Unsuccessful. Please check email and password', 'danger')
  return render_template("admin_login.html", title="Admin Login", form=form)

@login_required
@app.route("/admin/home")
def admin():
  page = request.args.get('page', 1, type=int)
  members = User.query.filter_by(role="USER").paginate(page=page, per_page=5)
  admins= User.query.filter_by(role="ADMIN").paginate(page=page, per_page=5)
  
  if current_user.role=="USER":
    return redirect(url_for('home'))
  return render_template("admin.html", title="Admin", members=members, admins=admins)


@login_required
@app.route("/admin/register-member", methods=["GET", "POST"])
def register_member():
  if current_user.role == "USER":
    return(redirect(url_for("home")))
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data, phone=form.phone.data)
    user.password = secrets.token_urlsafe(8)
    db.session.add(user)
    db.session.commit()
    flash(f"Account created for {form.username.data} successfully. Password for {form.username.data} is {user.password}", "success")
    return(redirect(url_for("admin")))
    
  return render_template("register_member.html", title="Register New Member", form=form)

@login_required
@app.route("/admin/register-admin", methods=["GET", "POST"])
def register_admin():
  if current_user.role == "USER":
    return(redirect(url_for("home")))
  elif current_user.is_superadmin==False:
    return(redirect(url_for("home")))
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data, phone=form.phone.data)
    user.password = secrets.token_urlsafe(8)
    db.session.add(user)
    db.session.commit()
    flash(f"Account created for {form.username.data} successfully. Password for {form.username.data} is {user.password}", "success")
    return(redirect(url_for("admin")))
    
  return render_template("register_admin.html", title="Register New Admin", form=form)

@login_required
@app.route('/admin/manage/<int:member_id>')
def view_member(member_id):
  if current_user.role == "ADMIN":
    member = User.query.get_or_404(member_id)
    return render_template('view_member.html', member=member)
  else:
    return redirect(url_for('home'))

@login_required
@app.route('/admin/manage/<int:member_id>/edit', methods=("GET", "POST"))
def edit_member(member_id):
  if current_user.role == "USER":
    return redirect(url_for('home'))
  member = User.query.get_or_404(member_id)

  form = UpdateMemberForm()
  form.current_member = member

  if form.validate_on_submit():
    if form.picture.data:
      picture_file = save_picture(form.picture.data)
      member.image_file = picture_file

    member.username = form.username.data
    member.email = form.email.data
    member.phone = form.phone.data
    member.password = form.password.data
    member.occupation = form.occupation.data
    member.experience = form.experience.data
    member.current_salary = form.current_salary.data
    
    db.session.add(member)
    db.session.commit()
    flash("Account successfuly modified", "success")
    return(redirect(url_for("view_member", member_id=member.id)))
  elif request.method == 'GET':
    form.username.data = member.username
    form.email.data = member.email
    form.phone.data = member.phone
    form.password.data = member.password
    form.occupation.data = member.occupation
    form.current_salary.data = member.current_salary
    form.experience.data = member.experience

  image_file = url_for('static', filename='profile_pics/' + member.image_file)
  return render_template('edit_member.html', member=member, form=form, image_file=image_file)

def send_reset_email(user):
  token = user.get_reset_token()
  msg = Message('Password Reset Request',
                sender='noreply@demo.com',
                recipients=[user.email])
  msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
  mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = RequestResetForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    send_reset_email(user)
    flash('An email has been sent with instructions to reset your password.', 'info')
    return redirect(url_for('home'))
  return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  user = User.verify_reset_token(token)
  if user is None:
    flash('That is an invalid or expired token', 'warning')
    return redirect(url_for('reset_request'))
  form = ResetPasswordForm()
  if form.validate_on_submit():
    user.password = form.password.data
    db.session.commit()
    flash('Your password has been updated! You are now able to log in', 'success')
    return redirect(url_for('home'))
  return render_template('reset_token.html', title='Reset Password', form=form)
