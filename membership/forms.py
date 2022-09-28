from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from membership.models import User, Unit

class UploadCsvForm(FlaskForm):
  csv_file = FileField('Upload CSV file', validators=[DataRequired(), FileAllowed(['csv',])])
  submit = SubmitField("Submit")


class UnitRegistrationForm(FlaskForm):
  name = StringField("Unit name", validators=[DataRequired(), Length(min=2,max=30)])
  amount = StringField("Fees", validators=[DataRequired(), Length(min=2,max=30)])
  submit = SubmitField("Submit")


class AdminRegistrationForm(FlaskForm):
  username = StringField("Username", validators=[DataRequired(), Length(min=2,max=20)])
  email = StringField("Email", validators=[DataRequired(), Email()])
  phone = StringField(validators=[DataRequired()])
  is_superadmin = BooleanField("Add as a super administrator")
  submit = SubmitField("Add Member")

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('That username is taken. Please choose a different one.')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError('That email is taken. Please choose a different one.')

  def validate_phone(self, phone):
    user = User.query.filter_by(phone=phone.data).first()
    if user:
      raise ValidationError('That phone number is taken. Please choose a different one.')


class UserRegistrationForm(FlaskForm):
  my_choices = []
  units = Unit.query.all()
  for unit in units:
    my_choices.append(unit.name)

  username = StringField("Username", validators=[DataRequired(), Length(min=2,max=20)])
  email = StringField("Email", validators=[DataRequired(), Email()])
  phone = StringField(validators=[DataRequired()])
  unit = SelectField("Unit", validators=[DataRequired()],choices=my_choices)
  submit = SubmitField("Add Member")

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('That username is taken. Please choose a different one.')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError('That email is taken. Please choose a different one.')

  def validate_phone(self, phone):
    user = User.query.filter_by(phone=phone.data).first()
    if user:
      raise ValidationError('That phone number is taken. Please choose a different one.')


class UserLoginForm(FlaskForm):
  phone = StringField(validators=[DataRequired()])
  password = PasswordField("Password", validators=[DataRequired()])
  remember = BooleanField("Remember me")
  submit = SubmitField("Log In")


class AdminLoginForm(FlaskForm):
  email = StringField(validators=[DataRequired(), Email()])
  password = PasswordField("Password", validators=[DataRequired()])
  remember = BooleanField("Remember me")
  submit = SubmitField("Log In")


class UpdateMemberForm(FlaskForm):
  my_choices = []
  units = Unit.query.all()
  for unit in units:
    my_choices.append(unit.name)

  username = StringField("Username", validators=[DataRequired(), Length(min=2,max=20)])
  email = StringField("Email", validators=[DataRequired(), Email()])
  picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
  phone = StringField(validators=[DataRequired()])
  password = StringField("Password", validators=[DataRequired()])
  unit = SelectField("Unit", validators=[DataRequired()],choices=my_choices)
  current_salary = StringField()
  occupation = StringField()
  home_address = StringField()
  date_of_birth = StringField()
  work_address = StringField()
  experience = StringField()
  submit = SubmitField("Edit Member")
  current_member = None

  def validate_username(self, username):
    if username.data != self.current_member.username:
      user = User.query.filter_by(username=username.data).first()
      if user:
        raise ValidationError('That username is taken. Please choose a different one.')

  def validate_email(self, email):
    if email.data != self.current_member.email:
      user = User.query.filter_by(email=email.data).first()
      if user:
        raise ValidationError('That email is taken. Please choose a different one.')

  def validate_phone(self, phone):
    if phone.data != self.current_member.phone:
      user = User.query.filter_by(phone=phone.data).first()
      if user:
        raise ValidationError('That phone number is taken. Please choose a different one.')


class UpdateAdminForm(FlaskForm):
  username = StringField("Username", validators=[DataRequired(), Length(min=2,max=20)])
  email = StringField("Email", validators=[DataRequired(), Email()])
  picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
  phone = StringField(validators=[DataRequired()])
  password = StringField("Password", validators=[DataRequired()])
  submit = SubmitField("Edit Member")
  current_member = None

  def validate_username(self, username):
    if username.data != self.current_member.username:
      user = User.query.filter_by(username=username.data).first()
      if user:
        raise ValidationError('That username is taken. Please choose a different one.')

  def validate_email(self, email):
    if email.data != self.current_member.email:
      user = User.query.filter_by(email=email.data).first()
      if user:
        raise ValidationError('That email is taken. Please choose a different one.')

  def validate_phone(self, phone):
    if phone.data != self.current_member.phone:
      user = User.query.filter_by(phone=phone.data).first()
      if user:
        raise ValidationError('That phone number is taken. Please choose a different one.')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

