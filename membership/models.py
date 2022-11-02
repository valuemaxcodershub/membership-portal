from membership import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from sqlalchemy.ext.hybrid import hybrid_property

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

user_unit = db.Table("user_unit",
  db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
  db.Column("unit_id", db.Integer, db.ForeignKey("unit.id")),
  )

#phone number is unique
class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  #db.backref fixes instrumentedlist error
  units = db.relationship("Unit", secondary=user_unit, backref=db.backref("unit_members", lazy='dynamic'), lazy="dynamic")
  username = db.Column(db.String(20), unique=True)
  email = db.Column(db.String(120), unique=True)
  phone = db.Column(db.String(60), unique=True)
  password = db.Column(db.String(60), nullable=False, default="12345678")
  image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
  date_registered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  role = db.Column(db.String(6), nullable=False, default="USER")
  _is_superadmin = db.Column("is_superadmin", db.Boolean, nullable=False, default=False)
  current_salary = db.Column(db.String(60))
  occupation = db.Column(db.String(60))
  experience = db.Column(db.String(60))
  date_of_birth = db.Column(db.String(77), nullable=False, default=datetime.utcnow)
  business_address = db.Column(db.String(120))
  _is_suspended = db.Column("is_suspended", db.Boolean, nullable=False, default=False)
  has_filled_profile = db.Column(db.Boolean(), default=False)
  business_name = db.Column(db.String(77))
  business_email = db.Column(db.String(120))
  business_phone = db.Column(db.String(77))
  business_photo = db.Column(db.String(20), default='default.jpg')
  business_about = db.Column(db.String(300))
  business_services = db.Column(db.String(300))
  #use image list
  business_product_image_1 = db.Column(db.String(20), nullable=False, default='default.jpg')
  business_product_image_2 = db.Column(db.String(20), nullable=False, default='default.jpg')
  business_product_image_3 = db.Column(db.String(20), nullable=False, default='default.jpg')
  business_product_image_4 = db.Column(db.String(20), nullable=False, default='default.jpg')
  business_product_image_5 = db.Column(db.String(20), nullable=False, default='default.jpg')
  business_product_image_6 = db.Column(db.String(20), nullable=False, default='default.jpg')
  business_facebook = db.Column(db.String(77))
  business_website = db.Column(db.String(77))
  business_twitter = db.Column(db.String(77))
  business_linkedin = db.Column(db.String(77))
  business_whatsapp = db.Column(db.String(77))
  messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
  messages_received = db.relationship('Message',
                                      foreign_keys='Message.member_recipient_id',
                                      backref='member_recipient', lazy='dynamic')
  last_message_read_time = db.Column(db.DateTime)


  def new_messages(self):
    last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
    #recipient should be units recieving
    # count = 0
    # for unit in self.units:
    #   count += Message.query.filter_by(recipient=unit).filter(
    #     Message.timestamp > last_read_time).count()

    # return count

    return Message.query.filter_by(recipient=self).filter(
        Message.timestamp > last_read_time).count()

  def display_units(self):
    unit_names = []
    for unit in self.units.all():
      unit_names.append(unit.name)

    return ", ".join(unit_names)

  #for csv export
  def unit_ids(self):
    unit_ids = []
    for unit in self.units.all():
      unit_ids.append(str(unit.id))

    return unit_ids

  
  @property
  def is_superadmin(self):
      return self._is_superadmin

  @property
  def is_suspended(self):
      return self._is_suspended

  @is_superadmin.setter
  def is_superadmin(self, s):
    #this exists because of the csv fuction that inputs strings
    if type(s) == type(str()):
      #change string to boolean
      if s.lower() == "true":
        self._is_superadmin = True
      elif s.lower() == "false":
        self._is_superadmin = False
    else:
      #dont change anything if it's not a string
      self._is_superadmin = s

  @is_suspended.setter
  def is_suspended(self, s):
    #this exists because of the csv fuction that inputs strings
    if type(s) == type(str()):
      #change string to boolean
      if s.lower() == "true":
        self._is_suspended = True
      elif s.lower() == "false":
        self._is_suspended = False
    else:
      #dont change anything if it's not a string
      self._is_suspended = s

  def get_reset_token(self, expires_sec=1800):
    s = Serializer(app.config['SECRET_KEY'], expires_sec)
    return s.dumps({'user_id': self.id}).decode('utf-8')

  @staticmethod
  def verify_reset_token(token):
      s = Serializer(app.config['SECRET_KEY'])
      try:
          user_id = s.loads(token)['user_id']
      except:
          return None
      return User.query.get(user_id)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Unit(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), unique=True, nullable=False)
  date_created = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
  fees_amount = db.Column(db.String(77),nullable=False,default="0")
  messages_received = db.relationship('Message',
                                      foreign_keys='Message.unit_recipient_id',
                                      backref='unit_recipient', lazy='dynamic')


  def __repr__(self):
    return f"Unit('{self.name}')"


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    member_recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    unit_recipient_id = db.Column(db.Integer, db.ForeignKey('unit.id'))
    title = db.Column(db.String(60))
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)
   

