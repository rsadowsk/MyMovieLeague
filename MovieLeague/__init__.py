from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import sendgrid

app = Flask(__name__, template_folder='templates')
app.config.from_object('app_config')

app.debug = app.config['DEBUG']
app.secret_key = app.config['SECRET_KEY']


## MAIL
SGMail = sendgrid.SendGridAPIClient(apikey=app.config['SENDGRID_API_KEY'])

## SQLALCHEMY
db = SQLAlchemy(app)

## Login Manager
login_manager = LoginManager()
login_manager.init_app(app)