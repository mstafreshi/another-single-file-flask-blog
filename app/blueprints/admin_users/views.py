from flask import render_template, flash, redirect, url_for, request, abort
from . import admin_users as bp
from ...models import User
from ... import db
from .forms import EditForm, EditPasswordForm, EditEmailForm, EditStatusForm
from sqlalchemy import desc

@bp.route('/list')
def list():
    users = User.query.order_by(desc(User.id)).all()
    data = dict(title="Users list", users=users)
    return render_template('admin_users/list.html', **data)
    
@bp.route('/edit/<int:id>/<what>', methods=["GET", "POST"])
def edit(id, what):
    forms = {
        'general' : (EditForm, "Edit user"),
        'password': (EditPasswordForm, "Edit user password"),
        'email'   : (EditEmailForm, "Edit user email"),
        'status'  : (EditStatusForm, "Edit user status"),
    }
    
    if what not in forms.keys():
        abort(404)
       
    user = User.query.get_or_404(id)
    active_form = forms[what][0] 
    form = active_form()
    if form.is_submitted():
        if form.validate():
            form.fill_data(user)
                       
            db.session.add(user)
            db.session.commit()
            
            flash("User editted successfully", category = "success")
            return redirect(url_for('admin_users.edit', id=user.id, what=what))
    else:
        form = active_form(obj=user)
                
    data = dict(title=forms[what][1], form=form, user=user)
    return render_template('admin_users/edit.html', **data)
    
