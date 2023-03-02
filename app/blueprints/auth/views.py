from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user
from .forms import LoginForm, RegisterForm
from . import auth as bp
from ... import db
from ...models import User

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index.index'))
        flash("Invalid username or password", category="danger")
    
    data = dict(title="Login", form=form)    
    return render_template('auth/login.html', **data)
    
@bp.route("/logout")
def logout():
    logout_user()
    flash("Successfuly logged out", category="success")
    return redirect(url_for('index.index'))
    
@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data
               
        user = User(username=username, name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registered successfully. Please Enter!', category='success')
        return redirect(url_for('auth.login'))
        
    data = dict(title="Register", form=form)
    return render_template('auth/register.html', **data)        
