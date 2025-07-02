from flask import Flask
from flask_migrate import Migrate
from flask_mail import Mail
from models import db

mail = Mail()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Email configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'emmanuelwambugu5@gmail.com' 
    app.config['MAIL_PASSWORD'] = 'lbwp xcmv djqk tvlk'         
    app.config['MAIL_DEFAULT_SENDER'] = 'emmanuelwambugu5@gmail.com' 

    db.init_app(app)
    Migrate(app, db)
    mail.init_app(app)

    # Register API routes
    from routes import api
    app.register_blueprint(api)

    return app
