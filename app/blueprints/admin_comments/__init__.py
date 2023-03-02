from flask import Blueprint

admin_comments = Blueprint('admin_comments', __name__)

from . import views
