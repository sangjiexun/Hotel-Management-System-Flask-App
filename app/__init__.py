from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Create app instance
app = Flask(__name__)
app.config.from_object('config')

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Import models and routes
from app.models import User, Team, Room, Meeting, CostLog, Participants_user, Participants_partner, Businesspartner
from app.routes import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))