from flask import Blueprint

bp = Blueprint('linkdump_categories', __name__)

from . import views
