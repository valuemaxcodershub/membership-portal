from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from membership.models import User

class UserAccountForm(FlaskForm):
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


class CreateProfileForm(FlaskForm):
  business_name = StringField("Business Name", validators=[DataRequired()])
  business_email = StringField("Business Email", validators=[DataRequired()])
  business_website = StringField("Website Url")
  business_phone = StringField("Business Phone Number", validators=[DataRequired()])
  business_about = TextAreaField("About your business")
  business_address = StringField("Business Location")
  business_services = TextAreaField("Services Rendered")
  business_facebook = StringField("Facebook")
  business_twitter = StringField("Twitter")
  business_linkedin = StringField("LinkedIn")
  business_whatsapp = StringField("Whatsapp")
  business_photo = FileField('Update Business Logo', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
  business_product_image_1 =  FileField('Display Picture 1', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
  business_product_image_2 =  FileField('Display Picture 2', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
  business_product_image_3 =  FileField('Display Picture 3', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
  business_product_image_4 =  FileField('Display Picture 4', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
  business_product_image_5 =  FileField('Display Picture 5', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
  business_product_image_6 =  FileField('Display Picture 6', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
  submit = SubmitField("Edit Form")


class UserLoginForm(FlaskForm):
  phone = StringField(validators=[DataRequired()])
  password = PasswordField("Password", validators=[DataRequired()])
  remember = BooleanField("Remember me")
  submit = SubmitField("Log In")