from flask import Blueprint

bp = Blueprint('linkdumps', __name__)

from . import views
