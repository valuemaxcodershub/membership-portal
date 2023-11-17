from flask import Blueprint, Response, render_template, redirect, url_for, abort, flash, request, send_file, make_response
from io import StringIO     # allows you to store response object in memory instead of on disk
import os
import json
from membership import app, db
from membership.admins.forms import MessageForm, UserRegistrationForm,  AdminLoginForm, UnitRegistrationForm, AdminRegistrationForm, UpdateMemberForm, UploadCsvForm, UpdateAdminForm
from membership.models import User, Unit, Message, UserUpdate
from membership.main.utils import save_picture
from membership.admins.utils import parse_csv
from flask_login import login_user, current_user, login_required, logout_user
import secrets
import csv
from sqlalchemy import or_
from membership.admins.utils import DataStore, admin_role_required, super_admin_role_required, add_member

admins = Blueprint("admins", __name__)


data = DataStore()


@admins.route('/admin/dues_pay', methods=['GET', 'POST'])
@admin_role_required
def dues_pay():
  
  return render_template("admin/dues_pay.html")

@admins.route('/admin/paid_dues', methods=['GET', 'POST'])
@admin_role_required
def paid_dues():
  
  return render_template("admin/paid-dues.html")

@admins.route('/admin/wallet', methods=['GET', 'POST'])
@admin_role_required
def wallet():
  
  return render_template("construction.html")

@admins.route('/admin/generate_finance', methods=['GET', 'POST'])
@admin_role_required
def generate_finance():
  
  return render_template("construction.html")

@admins.route('/admin/create_payment', methods=['GET', 'POST'])
@admin_role_required
def create_payment():

  return render_template("construction.html")


@admins.route('/admin/send_message', methods=['GET', 'POST'])
@admin_role_required
def send_message():
    recipient_id = int(request.form['user_id'])
    user = User.query.get_or_404(recipient_id)
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, member_recipient=user, title=form.title.data,
                      body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('admins.dashboard'))
    return render_template('admin/send_message.html', title=('Send Message'),
                           form=form, member_recipient=user)

@admins.route('/admin/send_unit_message', methods=['GET', 'POST'])
@admin_role_required
def send_unit_message():

    form = MessageForm()
 
    if form.validate_on_submit():

      selected_units = request.form.getlist('mymultiselect')

      inputted_units = []
      for unit_name in selected_units:
        unit = Unit.query.filter_by(name=unit_name).all()[0]
        inputted_units.append(unit)

      for unit in inputted_units:
        msg = Message(author=current_user, unit_recipient=unit, title=form.title.data,
                      body=form.message.data)
        db.session.add(msg)
        db.session.commit()

      flash('Your message has been sent.')
      return redirect(url_for('admins.dashboard'))


    return render_template('admin/send_message.html', title=('Send Message'),
                           form=form)

#this is for sending members to pages that don't use the dashboard layout e.g. business members
@admins.context_processor
def inject_menu():

    # Fill in with your actual menu dictionary:
    dashboard_units = Unit.query.all()

    return dict(dashboard_units=dashboard_units)


@admins.route("/home")
def home():
  if current_user.is_authenticated:
    if current_user.role == "ADMIN":
      return redirect(url_for('admins.dashboard'))

  return redirect(url_for("admins.admin_login"))

@admins.route("/admin-logout")
@admin_role_required
def admin_logout():
  logout_user()
  return redirect(url_for('admins.home'))


@admin_role_required
@admins.route('/_autocomplete', methods=['GET'])
def autocomplete():
    members = []
    for member in  User.query.filter_by(role="USER").all():
      members.append(member.username)
    return Response(json.dumps(members), mimetype='application/json')

@admin_role_required
@admins.route("/admin/search", methods=["POST"])
def search_members():
  query = request.form.get("search_query", False)
  page = request.args.get('page', 1, type=int)
  results = User.query.filter_by(role="USER").filter(or_(User.business_name.ilike(f'%{query}%'), User.business_phone.ilike(f'%{query}%'), User.business_email.ilike(f'%{query}%') ))
  data.a = results #add to datastore
  result_count = results.count()
  members = results.paginate(page=page, per_page=10)

  return render_template("search_results.html", result_count=result_count, members=members, query=query, title=f"Search Results for {query}")


@admins.route("/admin", methods=["GET", "POST"])
def admin_login():
  if current_user.is_authenticated:
    if current_user.role == "ADMIN":
      return redirect(url_for('admins.dashboard'))

  form = AdminLoginForm()
    
  
  if form.validate_on_submit():
    email_input = form.email.data
    password_input = form.password.data
    remember = form.remember.data
    admin = User.query.filter_by(role="ADMIN").filter_by(business_email=email_input).first()
    if admin and admin.password == password_input:
      login_user(admin, remember=remember)
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('admins.dashboard'))
    else:
      flash('Login Unsuccessful. Please check email and password', 'danger')
  return render_template("admin/admin_login.html", title="Admin Login", form=form)

#only for superadmin
@admins.route("/admin/manage_admins")
@super_admin_role_required
def manage_admins():
  page = request.args.get('page', 1, type=int)
  #return all admins except current admin
  admins= User.query.filter_by(role="ADMIN").filter(User.id!=current_user.id).paginate(page=page, per_page=10)

  return render_template("admin/manage_administrators.html", title="Admin Management", admins=admins)

@admins.route("/admin/manage_units")
@admin_role_required
def manage_units():
  page = request.args.get('page', 1, type=int)
  units= Unit.query.paginate(page=page, per_page=10)

  return render_template("admin/manage-units.html", title="Units Management", units=units)


@admins.route("/admin/edit_unit/<int:unit_id>", methods=["GET", "POST"])
@admin_role_required
def edit_unit(unit_id):
  unit = Unit.query.get_or_404(unit_id)

  form = UnitRegistrationForm()

  if form.validate_on_submit():
    unit.name = form.name.data
    db.session.add(unit)
    db.session.commit()
    return(redirect(url_for('admins.manage_units')))

  elif request.method == 'GET':
    form.name.data = unit.name


  return render_template("admin/edit-unit.html", form=form, unit=unit)

@admins.route("/admin/suspend_user", methods=['POST'])
@admin_role_required
def suspend_user():
  user_id = int(request.form['user_id'])
  user = User.query.get_or_404(user_id)
  user._is_suspended = not user._is_suspended
  page_num = request.form['page']

  db.session.add(user)
  db.session.commit()
  flash("Action Successful")
  return redirect(url_for('admins.manage_members', page=page_num))

@admins.route("/admin/delete_user", methods=['POST'])
@admin_role_required
def delete_user():
  user_id = int(request.form['user_id'])
  user = User.query.get_or_404(user_id)

  if user.role == "USER":
    link = 'admins.manage_members'
  else:
    link = 'admins.manage_admins'

  db.session.delete(user)
  db.session.commit()



  flash("User deleted successfuly")
  page_num = request.form['page']

  return redirect(url_for(link, page=page_num))

@admins.route("/admin/delete_unit", methods=['POST'])
@admin_role_required
def delete_unit():

  if request.form.get('unit_id'):
    unit_id = int(request.form['unit_id'])
    unit = Unit.query.get_or_404(unit_id)
    db.session.delete(unit)
    db.session.commit()
    flash("Unit deleted successfully")
  
  next_page = request.args.get('next')
  return redirect(next_page) if next_page else redirect(url_for('admins.manage_units'))



@admins.route("/admin/register-unit", methods=["GET", "POST"])
@admin_role_required
def register_unit():
  form = UnitRegistrationForm()

  if form.validate_on_submit():
    unit = Unit(name=form.name.data)
    db.session.add(unit)
    db.session.commit()
    flash(f"{form.name.data} Unit created successfuly", "success")
    return(redirect(url_for("admins.manage_units")))
  else:
    print("form not validated on submit")
    
  return render_template("admin/add_unit.html", title="Register New Unit", form=form)


#No member pagination because of model initialization 
#to do this, see https://stackoverflow.com/questions/46862900/why-i-am-getting-instrumentedlist-object-has-no-attribute-paginate-filter-by
@admins.route("/admin/manage_unit_members/<int:unit_id>")
@admin_role_required
def manage_unit_members(unit_id):
  page = request.args.get('page', 1, type=int)
  unit = Unit.query.filter_by(id=unit_id)[0]
  unit_members = unit.unit_members
  print(unit_members)
  members = unit_members

  return render_template("admin/manage_unit_members.html", title="Units Management", members=members, unit=unit)


@admins.route("/admin/register-member", methods=["GET", "POST"])
@admin_role_required
def register_member():
  if current_user.role == "USER":
    return(redirect(url_for("admins.home")))
  form = UserRegistrationForm()
  all_units = Unit.query.all()

  if form.validate_on_submit():
    add_member(form.phone.data)
    return(redirect(url_for("admins.manage_members")))
    
  return render_template("admin/add-member.html", title="Register New Member", form=form, units=all_units)


@admins.route('/admin/export-custom', methods=["POST"])
@admin_role_required
def export_custom():
  si = StringIO()
  cw = csv.writer(si)
  records = data.a.all() #fetch from data store
  if records:
    print(records[0].unit_ids())
  cw.writerow(["business_name", "phone", "email", "unit_ids"])
  cw.writerows([( r.business_name, r.business_phone, r.business_email, "-".join(r.unit_ids()) ) for r in records])
  response = make_response(si.getvalue())
  response.headers['Content-Disposition'] = 'attachment; filename=report.csv'
  response.headers["Content-type"] = "text/csv"
  return response


@admins.route("/admin/register-bulk", methods=["GET", "POST"])
@admin_role_required
def register_bulk(error_message=""):

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
      return(redirect(url_for("admins.manage_members")))

  return render_template("admin/register_bulk.html", form=form, error_message=error_message)



@admins.route("/admin/dashboard")
@admins.route("/admin/home")
@admin_role_required
def dashboard():
  total_members = User.query.filter_by(role="USER").count()
  total_units = Unit.query.count()

  return render_template("admin/index.html", total_members=total_members,
                                       total_units=total_units,
                                        )

@admins.route("/admin/manage_members")
@admin_role_required
def manage_members():
  form = MessageForm()
  page = request.args.get('page', 1, type=int)
  results = User.query.filter_by(role="USER")
  members = results.paginate(page=page, per_page=10)

  # exporting
  data.a = results

  return render_template("admin/manage_members.html", form=form, page=page, members=members)



@admins.route('/admin/approved_profiles')
@super_admin_role_required
def approved_profiles():
  form = MessageForm()
  user_updates = UserUpdate.query.filter_by(update_status = UserUpdate.APPROVED)
  page = request.args.get('page', 1, type=int)
  approved_updates_list = user_updates.paginate(page=page, per_page=10)

  return render_template('admin/approved_profiles.html', members = approved_updates_list, form=form)


@admins.route('/admin/disapproved_profiles')
@super_admin_role_required
def disapproved_profiles():
  form = MessageForm()
  user_updates = UserUpdate.query.filter_by(update_status = UserUpdate.DISAPPROVED)
  page = request.args.get('page', 1, type=int)
  disapproved_updates_list = user_updates.paginate(page=page, per_page=10)

  return render_template('admin/disapproved_profiles.html', members = disapproved_updates_list, form=form)


@admins.route('/admin/pending_approvals', methods=['GET', 'POST'])
@super_admin_role_required
def pending_approvals():
  form = MessageForm()
  user_updates = UserUpdate.query.filter_by(update_status = UserUpdate.PENDING)
  page = request.args.get('page', 1, type=int)
  pending_updates_list = user_updates.paginate(page=page, per_page=10)


  if request.method == 'POST':
    if request.form.get('profile_updateid'):
      profileid = request.form.get('profile_updateid')
      user_update = UserUpdate.query.filter_by(id = profileid)[0]
      owner_of_update = User.query.filter_by(id = user_update.userid)[0]
      user_data = json.loads(user_update.update)
      
      for key, value in user_data.items():
        setattr(owner_of_update, key, value)
        
      if user_data.get('selected_units'):
          add_member(owner_of_update.business_phone, user_data.get('selected_units'))
          
      owner_of_update.has_filled_profile = True
      owner_of_update.update_is_approved = User.USER_UPDATE_APPROVED
      user_update.update_status = UserUpdate.APPROVED
      db.session.add_all([owner_of_update, user_update])
      db.session.commit()

      
    if request.form.get('profile_updateid_disapprove'):
      profileid = request.form.get('profile_updateid_disapprove')
      user_update = UserUpdate.query.filter_by(id = profileid)[0]
      owner_of_update = User.query.filter_by(id = user_update.userid)[0]
      owner_of_update.update_is_approved = User.USER_UPDATE_DISAPPROVED
      user_update.update_status = UserUpdate.DISAPPROVED
      db.session.add(user_update)
      db.session.commit()

    return redirect(url_for('admins.pending_approvals'))

  return render_template('admin/pending_approvals.html', pending_updates_list = pending_updates_list, form=form)



@admins.route("/admin/register-admin", methods=["GET", "POST"])
@super_admin_role_required
def register_admin():
  if current_user.role == "USER":
    return(redirect(url_for("admins.home")))
  elif current_user.is_superadmin==False:
    return(redirect(url_for("admins.home")))
  form = AdminRegistrationForm()

  
  if form.validate_on_submit():
    user = User(business_email=form.email.data)
    user.role = "ADMIN"
    if form.is_superadmin.data:
      user.is_superadmin = True
    # user.password = secrets.token_urlsafe(8)
    db.session.add(user)
    db.session.commit()
    flash(f"Account created for {form.email.data} successfully. Password for {form.email.data} is {user.password}", "success")
    return(redirect(url_for("admins.manage_admins")))

  return render_template("admin/add_admin.html", title="Register New Admin", form=form)


@admins.route('/admin/manage/<int:member_id>')
@login_required
def view_member(member_id):
  if current_user.role == "ADMIN":
    member = User.query.get_or_404(member_id)
    return render_template('profile.html', member=member)
  else:
    return redirect(url_for('admins.home'))


@admins.route('/admin/manage_admin/<int:admin_id>/edit', methods=("GET", "POST"))
@admins.route('/admin/account')
@login_required
def edit_admin(admin_id):
  admin = User.query.get_or_404(admin_id)

  form = UpdateAdminForm()
  form.current_member = admin

  if form.validate_on_submit():
    if form.picture.data:
      picture_file = save_picture(form.picture.data)
      admin.business_photo = picture_file

    admin.username = form.username.data
    admin.business_email = form.email.data
    admin.business_phone = form.phone.data
    admin.password = form.password.data
    
    db.session.add(admin)
    db.session.commit()
    flash("Account successfuly modified", "success")
    return(redirect(url_for("admins.manage_admins", member_id=admin.id)))
  
  elif request.method == 'GET':
    form.username.data = admin.username
    form.email.data = admin.business_email
    form.phone.data = admin.business_phone
    form.password.data = admin.password

  image_file = url_for('static', filename='profile_pics/' + str(admin.business_photo))
  return render_template('admin/edit_admin_detail.html', admin=admin, form=form, image_file=image_file)



#implement select multiple units
#user can have multiple units but the form doesn't show that,
#it makes it look like the user can pick just 1 unit
@admins.route('/admin/manage/<int:member_id>/edit', methods=("GET", "POST"))
@login_required
def edit_member(member_id):
  if current_user.role == "USER":
    return redirect(url_for('admins.home'))
  member = User.query.get_or_404(member_id)

  form = UpdateMemberForm()
  units = Unit.query.all()
  form.current_member = member

  if form.validate_on_submit():

    if form.picture.data:
      picture_file = save_picture(form.picture.data)
      member.business_photo = picture_file

    member.password = form.password.data
    member.business_name = form.business_name.data
    member.business_about = form.business_about.data
    member.business_email = form.email.data
    member.business_about = form.business_about.data
    member.business_address = form.business_address.data
    member.business_phone = form.phone.data
    member.date_of_birth = form.date_of_birth.data

    selected_units = request.form.getlist('mymultiselect')

    inputted_units = []
    for unit_name in selected_units:
      unit = Unit.query.filter_by(name=unit_name).all()[0]
      inputted_units.append(unit)

    for d in member.units:
      member.units.remove(d)
    
    for unit in inputted_units:
      member.units.append(unit)
    
    db.session.add(member)
    db.session.commit()
    flash("Account successfully modified", "success")
    
    return(redirect(url_for("admins.manage_members")))
  

  elif request.method == 'GET':
    form.password.data = member.password
    form.date_of_birth.data = member.date_of_birth
    form.business_about.data = member.business_about
    form.business_name.data = member.business_name
    form.email.data = member.business_email
    form.business_address.data = member.business_address
    form.phone.data = member.business_phone
    
    db.session.add(member)
    db.session.commit()

  image_file = url_for('static', filename='profile_pics/' + member.business_photo)
  return render_template('admin/edit_member_detail.html', member=member, form=form, image_file=image_file, units=units)

@admins.route('/admin/download-template')
@admin_role_required
def download_template():
  template_list = ["phone"]
  
  print(",".join(template_list))

  template_csv_path = os.path.join(app.root_path, 'static/CSVs/template.csv')

  with open(template_csv_path, "w") as f:
    f.write(",".join(template_list))

  return send_file( template_csv_path, mimetype='text/csv', download_name='nasme_bulk_template.csv', as_attachment=True )

@admins.route('/admin/export-database')
@admin_role_required
def export_db():
  si = StringIO()
  cw = csv.writer(si)
  records = User.query.all()   # or a filtered set, of course
  # any table method that extracts an iterable will work
  cw.writerow(["phone", "business_name", "business_phone", "business_email", "businesss_about", "unit_ids", "image_file", "business_about", "business_address", "experience", "date_of_birth"])
  cw.writerows([(r.phone, r.business_name, r.business_phone, r.business_email, r.business_about, "-".join(r.unit_ids()), r.image_file, r.business_about, r.occupation, r.business_address, r.date_of_birth) for r in records])
  response = make_response(si.getvalue())
  response.headers['Content-Disposition'] = 'attachment; filename=report.csv'
  response.headers["Content-type"] = "text/csv"
  return response
