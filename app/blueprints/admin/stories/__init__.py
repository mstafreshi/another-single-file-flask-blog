from flask import Blueprint

bp = Blueprint("stories", __name__)

from . import views
