from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import config

bootstrap = Bootstrap5()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    
    from .blueprints.index import index
    from .blueprints.auth import auth
    from .blueprints.errors import error
    from .blueprints.admin_posts import admin_posts
    from .blueprints.admin_users import admin_users
    from .blueprints.admin_comments import admin_comments
    
    app.register_blueprint(index)
    app.register_blueprint(auth, url_prefix='/auth')    
    app.register_blueprint(error)
    app.register_blueprint(admin_posts, url_prefix='/admin/posts')
    app.register_blueprint(admin_users, url_prefix='/admin/users')
    app.register_blueprint(admin_comments, url_prefix='/admin/comments')
    return app
