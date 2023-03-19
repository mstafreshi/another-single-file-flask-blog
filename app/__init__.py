from flask import Flask, request, g
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_babel import Babel
from flask_pagedown import PageDown
from .config import config

bootstrap = Bootstrap5()
babel = Babel()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

pagedown = PageDown()

def get_locale():
    return g.lang_code
       
def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app, locale_selector=get_locale)
    pagedown.init_app(app)
    
    from .blueprints.user import user
    from .blueprints.admin import admin
       
    app.register_blueprint(user)
    app.register_blueprint(admin, url_prefix='/admin')
    
    return app
