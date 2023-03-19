from flask import Blueprint, abort, redirect, url_for, g
from flask_login import current_user, login_required

admin = Blueprint('admin', __name__)

from .posts import bp as posts
from .users import bp as users
from .comments import bp as comments
from .linkdump_categories import bp as linkdump_categories
from .linkdumps import bp as linkdumps
    
admin.register_blueprint(posts, url_prefix='/posts')
admin.register_blueprint(users, url_prefix='/users')
admin.register_blueprint(comments, url_prefix='/comments')
admin.register_blueprint(linkdump_categories, url_prefix='/linkdump-categories')
admin.register_blueprint(linkdumps, url_prefix='/linkdumps')

@admin.before_request
def before_request():
    if not current_user.is_authenticated:
        return redirect(url_for('user.auth.login', lang_code=g.lang_code))
                   
    if not current_user.is_administrator():
        abort(403)
