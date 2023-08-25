from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from flask_login import LoginManager


app = Flask(__name__)

db = SQLAlchemy()
DB_NAME = "bodabodainsurance.sqlite3"
app.config['SECRET_KEY'] = 'thequickbrownfoxjumpsoverthelazydog'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), DB_NAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


from flaskapp.models import User, Booking
with app.app_context():
    db.create_all()


from flaskapp.users.routes import users
from flaskapp.booking.routes import booking
from flaskapp.main.routes import main
app.register_blueprint(users)
app.register_blueprint(booking)
app.register_blueprint(main)
