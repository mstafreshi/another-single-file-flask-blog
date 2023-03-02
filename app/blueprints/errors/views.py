from flask import render_template
from . import error as bp

@bp.app_errorhandler(404)
def page_not_found(err):
    data = dict(title="Page not found")
    return render_template('errors/404.html', **data)
    
@bp.app_errorhandler(500)
def internal_server_error(err):
    data = dict(title="Internal server error")
    return render_template('errors/500.html', **data)
 
#access forbidden   
@bp.app_errorhandler(403)
def access_forbidden(err):
    data = dict(title="Access forbidden")
    return render_template("errors/403.html", **data)
