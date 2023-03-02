from flask import Blueprint

admin_posts = Blueprint('admin_posts', __name__)

from . import views
