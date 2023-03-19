from flask import render_template
from flask_babel import _
from . import bp

@bp.app_errorhandler(404)
def page_not_found(err):
    data = dict(title=_("Page not found"))
    return render_template('user/error/404.html', **data)
    
@bp.app_errorhandler(500)
def internal_server_error(err):
    data = dict(title=_("Internal server error"))
    return render_template('user/error/500.html', **data)
 
#access forbidden   
@bp.app_errorhandler(403)
def access_forbidden(err):
    data = dict(title=_("Access forbidden"))
    return render_template("user/error/403.html", **data)
