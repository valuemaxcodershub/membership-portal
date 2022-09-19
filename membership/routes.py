from flask import render_template, redirect, url_for, flash, request, abort
import os
from PIL import Image
from membership import app, db, bcrypt, mail
from membership.forms import UserRegistrationForm, UserLoginForm, AdminLoginForm, AdminRegistrationForm, UpdateMemberForm, RequestResetForm, ResetPasswordForm, UploadCsvForm
from membership.models import User, Unit
from flask_login import login_user, current_user, logout_user, login_required
import secrets
from flask_mail import Message
import csv
from wtforms.validators import DataRequired, ValidationError
from functools import wraps

def admin_role_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.role == "ADMIN":
            abort(403)
        return func(*args, **kwargs)
    return decorated_view

def super_admin_role_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_superadmin:
            abort(403)
        return func(*args, **kwargs)
    return decorated_view


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
def login():
  if current_user.is_authenticated:
      return redirect(url_for('home'))
  form = UserLoginForm()


  if request.method == "POST":
    phone_input = request.form['phone']
    password_input = request.form['password']
    user = User.query.filter_by(phone=phone_input).first()
    if user and user.password == password_input:
      login_user(user)
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('home'))
    else:
      flash('Login Unsuccessful. Please check Phone number and password', 'danger')
    
  return render_template("user_login.html", title="Login", form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
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
    email_input = form.email.data
    password_input = form.password.data
    admin = User.query.filter_by(role="ADMIN").filter_by(email=email_input).first()
    if admin and admin.password == password_input:
      login_user(admin)
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('dashboard'))
    else:
      flash('Login Unsuccessful. Please check email and password', 'danger')
  return render_template("admin_login.html", title="Admin Login", form=form)


@app.route("/admin/home")
@login_required
def admin():
  page = request.args.get('page', 1, type=int)
  members = User.query.filter_by(role="USER").paginate(page=page, per_page=5)
  
  if current_user.role=="USER":
    return redirect(url_for('home'))
  return render_template("admin.html", title="Admin", members=members)

#only for superadmin
@app.route("/admin/manage_admins")
@super_admin_role_required
@login_required
def manage_admins():
  page = request.args.get('page', 1, type=int)
  admins= User.query.filter_by(role="ADMIN").paginate(page=page, per_page=5)

  return render_template("manage_administrators.html", title="Admin Management", admins=admins)


@app.route("/admin/manage_units")
@admin_role_required
@login_required
def manage_admins():
  page = request.args.get('page', 1, type=int)
  units= Unit.query.all().paginate(page=page, per_page=5)

  return render_template("manage-units.html", title="Units Management", units=units)



@app.route("/admin/register-member", methods=["GET", "POST"])
@login_required
@admin_role_required
def register_member():
  if current_user.role == "USER":
    return(redirect(url_for("home")))
  form = UserRegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data, phone=form.phone.data)
    unit = Unit.query.filter_by(name=form.unit.data).all()[0]
    user.units.append(unit)
    user.password = secrets.token_urlsafe(8)
    db.session.add(user)
    db.session.commit()
    flash(f"Account created for {form.username.data} successfully. Password for {form.username.data} is {user.password}", "success")
    return(redirect(url_for("admin")))
    
  return render_template("add-member.html", title="Register New Member", form=form)


def parse_csv(csv_file):
  with open(csv_file) as csv_file:
    csv_reader = csv.DictReader(csv_file)

    #compulsory items
    params = User.__dict__
    #items that are not to be set from the file
    if current_user.is_superadmin:
      bad_params = ["id", "date_registered"]
    else:
      bad_params = ["id", "date_registered", "role", "is_superadmin"]


    for row in csv_reader:
      user = User()
      #Set the values of the items that exist in class
      for key, value in row.items():
        if key in params:
          if key in bad_params:
            raise ValueError(f'Either the "{key}" column doesn\'t exist in the database, or you don\'t have the required permission to access this field.')
          else: #assign if all columns are eligible
            print(f"{key} =  {value}")
            setattr(user, key, value)

      db.session.add(user)

    

# @login_required
# @app.route("/admin/register-bulk", methods=["GET", "POST"])
# def register_bulk():
#   if current_user.role == "USER":
#     return(redirect(url_for("home")))
#   form = UploadCsvForm()
#   if form.validate_on_submit():
#     file = request.files['file']
#     csv_path = os.path.join(app.root_path, 'static/CSVs', file.filename)
#     file.save(csv_path)

#     parse_csv(csv_path)
#     flash("Bulk registration successful")
#     return(redirect(url_for("admin")))

#   return render_template("register_bulk.html", form=form)


@app.route("/admin/register-bulk", methods=["GET", "POST"])
@login_required
def register_bulk(error_message=""):
  if current_user.role == "USER":
    return(redirect(url_for("home")))
  form = UploadCsvForm()

  if form.validate_on_submit():
    file = form.csv_file.data
    csv_path = os.path.join(app.root_path, 'static/CSVs', file.filename)
    file.save(csv_path)

    #bulk registration
    try:
      parse_csv(csv_path)
      db.session.commit()
    except Exception as e:
      db.session.remove()
      error_message = f"There is an error with the input file -> \n{e}"
      return render_template("register_bulk.html", form=form, error_message=error_message)
    else:
      flash("Bulk registration successful")
      return(redirect(url_for("admin")))

  return render_template("register_bulk.html", form=form, error_message=error_message)



@app.route("/admin/dashboard")
@admin_role_required
@login_required
def dashboard():
  total_members = len(User.query.filter_by(role="USER").all())
  return render_template("index.html", total_members=total_members)

@app.route("/admin/manage_members")
@admin_role_required
@login_required
def manage_members(unit_id=None):
  #search for unit members if the request is for a particular unit
  if unit_id:
    unit = Unit.query.filter_by(id=unit_id)
    unit_members = unit.unit_members[0]

    members = unit_members.paginate(page=page, per_page=5)

  else: #just return all members
    members = User.query.filter_by(role="USER").paginate(page=page, per_page=5)

  page = request.args.get('page', 1, type=int)
  
  

  return render_template("manage_members.html", page=page, members=members)




@app.route("/admin/register-admin", methods=["GET", "POST"])
@login_required
def register_admin():
  if current_user.role == "USER":
    return(redirect(url_for("home")))
  elif current_user.is_superadmin==False:
    return(redirect(url_for("home")))
  form = AdminRegistrationForm()

  
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data, phone=form.phone.data)
    user.role = "ADMIN"
    if form.is_superadmin:
      user.is_superadmin = True
    user.password = secrets.token_urlsafe(8)
    db.session.add(user)
    db.session.commit()
    flash(f"Account created for {form.username.data} successfully. Password for {form.username.data} is {user.password}", "success")
    return(redirect(url_for("admin")))

    
  return render_template("add_admin.html", title="Register New Admin", form=form)


@app.route('/admin/manage/<int:member_id>')
@login_required
def view_member(member_id):
  if current_user.role == "ADMIN":
    member = User.query.get_or_404(member_id)
    return render_template('view_member.html', member=member)
  else:
    return redirect(url_for('home'))


@app.route('/admin/manage/<int:member_id>/edit', methods=("GET", "POST"))
@login_required
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
  if request.method == "POST":
    email_input = request.form['email']
    user = User.query.filter_by(email=email_input).first()
    if user:
      send_reset_email(user)
      flash('An email has been sent with instructions to reset your password.', 'info')
      return redirect(url_for('home'))
    else:
      flash('There is no account with that email. You must register first.', 'info')
  return render_template('reset_request.html', title='Reset Password')


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
