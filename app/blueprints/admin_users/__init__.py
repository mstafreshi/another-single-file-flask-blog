from flask import Blueprint

admin_users = Blueprint('admin_users', __name__)

from . import views
