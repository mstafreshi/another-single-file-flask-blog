from flask import render_template, flash, redirect, url_for
from flask_babel import _
from flask_login import current_user
from .forms import LinkForm
from ....models import Linkdump, LinkdumpCategory
from .... import db
from . import bp

@bp.route("/list/<int:category_id>")
def list(category_id):
    category = LinkdumpCategory.query.get_or_404(category_id)
    if not category.links.count():
        return redirect(url_for('admin.linkdumps.link', category_id=category.id))
        
    navigation = [
        {
            'text': _('Add link'), 
            'link': url_for('admin.linkdumps.link', category_id=category.id)
        },
        {
            'text': _('Edit category'), 
            'link': url_for('admin.linkdump_categories.category', id=category.id)
        },
        {
            'text': _('Categories list'), 
            'link': url_for('admin.linkdump_categories.list')
        }, 
    ]
       
    data = dict(title=category.name, category=category, navigation=navigation)
    return render_template("admin/linkdumps/list.html", **data)
    
@bp.route('/link/<int:category_id>/<int:id>', methods=["GET", "POST"])  
@bp.route('/link/<int:category_id>', defaults={'id': None}, methods=["GET", "POST"])
def link(category_id, id):
    if id is None:
        link = Linkdump()
        link.category = LinkdumpCategory.query.get_or_404(category_id)
        link.creator = current_user._get_current_object()
    else:
        link = Linkdump.query.get_or_404(id)        
        if link.category.id != category_id:
            abort(404)
            
    form = LinkForm()
    
    if form.is_submitted():
        if form.validate():
            link.text = form.text.data.strip()
            link.alt = form.alt.data.strip()
            link.link = form.link.data.strip()
         
            db.session.add(link)
            db.session.commit()
            flash(_("Link added successfully"), category="success")
            return redirect(url_for('.list', category_id=link.category.id))   
    
    form = LinkForm(obj=link)
    form.category.data = link.category.name
    
    navigation = [
        {
            'text': _('Back to') + " " + link.category.name,
            'link': url_for('.list', category_id=link.category.id)
        }    
    ]
    
    title = _('Edit link') if link.id else _('Add link')             
    data=dict(title=title, form=form, navigation=navigation)
    return render_template("admin/linkdumps/link.html", **data)
    
@bp.route("/delete/<int:id>")
def delete(id):
    link = Linkdump.query.get_or_404(id)
    db.session.delete(link)
    db.session.commit()
    
    flash(_("Link deleted successfully."), category="success")
    return redirect(url_for('.list', category_id=link.linkdump_category_id))
