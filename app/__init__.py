import os

from flask import Flask, render_template
from flask_login import LoginManager
from flask_sendgrid import SendGrid
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect

from config import config

db = SQLAlchemy()
mail = SendGrid()
csrf = CsrfProtect()

# Set up Flask-login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.signin'


def create_app(config_name):
    '''For to use dynamic environment'''
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    #  # HTTP error handling
    #  @app.errorhandler(404)
    #  def not_found(error):
    #      return render_template('error/404.html'), 404

    #  @app.errorhandler(500)
    #  def internal_server_error(error):
    #      return render_template('error/500.html'), 500

    # Import a module / component using its blueprint handler variable
    from app.auth.controllers import mod as auth_module
    from app.forc.controllers import mod as forc_module

    # Register blueprint(s)
    # app.register_blueprint(xyz_module)
    app.register_blueprint(auth_module)
    app.register_blueprint(forc_module)

    return app
