from flask import Flask, request, g
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_babel import Babel, lazy_gettext as _l
from .config import config

bootstrap = Bootstrap5()
babel = Babel()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_message = _l("For access to this page, please login.")
login_manager.login_message_category = 'danger'
# I have decorated a function in auth views file with 
# @login_manager.unauthorized_handler. Therefore we do'nt no need to this.
#login_manager.login_view = 'user.auth.login'

def get_locale():
    return g.lang_code
       
def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app, locale_selector=get_locale)
    
    from .blueprints.user import user
    from .blueprints.admin import admin
       
    app.register_blueprint(user)
    app.register_blueprint(admin, url_prefix='/admin')
    
    return app
