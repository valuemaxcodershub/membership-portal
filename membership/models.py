from membership import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from sqlalchemy.ext.hybrid import hybrid_property

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

user_unit = db.Table("user_unit",
  db.Column("user_id", db.Integer, db.ForeignKey("unit.id")),
  db.Column("unit_id", db.Integer, db.ForeignKey("user.id")),
  )

#phone number is unique
class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  units = db.relationship("Unit", secondary=user_unit, backref="unit_members", lazy="dynamic")

  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  phone = db.Column(db.String(60), unique=True, nullable=False, default="")
  password = db.Column(db.String(60), nullable=False, default="~~~~~~~")
  image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
  date_registered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  role = db.Column(db.String(6), nullable=False, default="USER")
  _is_superadmin = db.Column("is_superadmin", db.Boolean, nullable=False, default=False)
  current_salary = db.Column(db.String(60))
  occupation = db.Column(db.String(60))
  experience = db.Column(db.String(60))
  date_of_birth = db.Column(db.String(), nullable=False, default=datetime.utcnow)
  home_address = db.Column(db.String())
  work_address = db.Column(db.String())

  
  @property
  def is_superadmin(self):
      return self._is_superadmin

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
  fees_amount = db.Column(db.String(),nullable=False,default="0")


  def __repr__(self):
    return f"Unit('{self.name}')"
   

