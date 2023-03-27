from flask import render_template, flash, redirect, url_for, request, g, current_app
from flask_babel import _
from flask_login import login_user, logout_user, current_user
from .forms import LoginForm, RegisterForm
from . import bp
from .... import db
from ....models import User, Role
from .... import login_manager

@login_manager.unauthorized_handler
def unauthorized():
    # I don't know why I need to call flash explicitly!
    flash(login_manager.login_message, category=login_manager.login_message_category)
    return redirect(url_for("user.auth.login", lang_code=g.lang_code))
    
@bp.route("/<lang_code>/login", methods=["GET", "POST"])
def login(lang_code):
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') \
                or url_for('user.index.index', lang_code=g.lang_code if \
                    g.lang_code != current_app.config.get('DEFAULT_LANG_CODE') else None)
                )
        flash(_("Invalid username or password"), category="danger")
    
    data = dict(title=_("Login"), form=form)    
    return render_template('user/auth/login.html', **data)
    
@bp.route("/logout")
def logout():
    logout_user()
    flash(_("Successfuly logged out"), category="success")
    return redirect(url_for('user.index.index', lang_code=g.lang_code if \
        g.lang_code != current_app.config.get('DEFAULT_LANG_CODE') else None)
    )
    
@bp.route("/<lang_code>/register", methods=["GET", "POST"])
def register(lang_code):    
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data                                           
        user = User(username=username, name=name, email=email, password=password, \
            lang_code=g.lang_code)        
         
        if email == current_app.config.get('ADMINISTRATOR_EMAIL'):
            user.role = Role.query.filter_by(name="Administrator").first()
        else:
            user.role = Role.query.filter_by(name="Registered_user").first()
           
        db.session.add(user)
        db.session.commit()
        
        flash(_('Registered successfully. Please Enter.'), category='success')
        return redirect(url_for('user.auth.login', lang_code=g.lang_code))
        
    data = dict(title=_("Register"), form=form)
    return render_template('user/auth/register.html', **data)        
