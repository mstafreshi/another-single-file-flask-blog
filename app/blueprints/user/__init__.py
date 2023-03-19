from flask import Blueprint, g, current_app, request
from flask_login import current_user

user = Blueprint('user', __name__)

from .index import bp as index
from .auth import bp as auth
from .error import bp as error

user.register_blueprint(index)
user.register_blueprint(auth)
user.register_blueprint(error)

@user.before_app_request
def before_request():
    g.lang_code = request.view_args.get('lang_code', current_user.get_lang_code())