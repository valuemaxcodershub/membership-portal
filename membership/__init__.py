from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from sqlalchemy import MetaData
import os
from dotenv import load_dotenv

load_dotenv()


user = 'root'
password = ''

#i added a comment
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "0f3c34f7789f6917e12593945aa86bdb"
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('NASME_DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user}:{password}@localhost/nasme'


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'members.login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)
migrate = Migrate(app, db)


from membership.members.routes import members
from membership.admins.routes import admins
from membership.main.routes import main

app.register_blueprint(members)
app.register_blueprint(admins)
app.register_blueprint(main)

with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch= True)
    else:
        migrate.init_app(app, db)
        print('About to migrate to db')