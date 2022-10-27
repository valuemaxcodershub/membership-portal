from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class CreateProfileForm(FlaskForm):
  business_name = StringField("Business Name", validators=[DataRequired()])
  business_email = StringField("Business Email", validators=[DataRequired()])
  business_website = StringField("Website Url")
  business_phone = StringField("Business Phone Number", validators=[DataRequired()])
  business_about = StringField("About your business")
  business_address = StringField("Business Location")
  business_services = StringField("Services Rendered")
  business_facebook = StringField("Facebook")
  business_twitter = StringField("Twitter")
  business_linkedin = StringField("LinkedIn")
  business_whatsapp = StringField("Whatsapp")
  business_photo = FileField('Update Business Picture', validators=[FileAllowed(['jpg', 'png'])])
  business_product_image_1 =  FileField('Display Picture 1', validators=[FileAllowed(['jpg', 'png'])])
  business_product_image_2 =  FileField('Display Picture 2', validators=[FileAllowed(['jpg', 'png'])])
  business_product_image_3 =  FileField('Display Picture 3', validators=[FileAllowed(['jpg', 'png'])])
  business_product_image_4 =  FileField('Display Picture 4', validators=[FileAllowed(['jpg', 'png'])])
  business_product_image_5 =  FileField('Display Picture 5', validators=[FileAllowed(['jpg', 'png'])])
  business_product_image_6 =  FileField('Display Picture 6', validators=[FileAllowed(['jpg', 'png'])])
  submit = SubmitField("Edit Form")


class UserLoginForm(FlaskForm):
  phone = StringField(validators=[DataRequired()])
  password = PasswordField("Password", validators=[DataRequired()])
  remember = BooleanField("Remember me")
  submit = SubmitField("Log In")