from flask import render_template, flash, redirect, url_for, request, abort
from flask_babel import _
from ....models import User
from .... import db
from .forms import EditForm, PasswordForm
from sqlalchemy import desc
from . import bp

@bp.route('/list')
def list():
    users = User.query.order_by(desc(User.id)).all()
    data = dict(title=_("Users list"), users=users)
    return render_template('admin/users/list.html', **data)
    
@bp.route('/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
    user = User.query.get_or_404(id)
    form = EditForm()    
    if form.is_submitted():
        if form.validate():
            form.fill_data(user)
                       
            db.session.add(user)
            db.session.commit()
            
            flash(_("User editted successfully"), category = "success")
            return redirect(url_for('admin.users.edit', id=user.id))
    else:
        form = EditForm(obj=user)
    
    navigation = [
        {'text': _('Users list'), 'link': url_for('.list')}    
    ]           
    data = dict(title=_("Edit user") + " " + user.username, form=form, user=user, navigation=navigation)
    return render_template('admin/users/edit.html', **data)
    
@bp.route('/password/<int:id>', methods=["GET", "POST"])
def password(id):
    user = User.query.get_or_404(id)
    form = PasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        
        flash(_("User password changed successfully."), category="success")
        return redirect(url_for('.password', id=user.id))
        
    data = dict(title=_("Edit password of") + " " + user.username, form=form, user=user)
    return render_template('admin/users/password.html', **data)   
