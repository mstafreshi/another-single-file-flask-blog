from flask import render_template, url_for, flash, redirect
from flask_babel import _
from ....models import LinkdumpCategory
from .forms import CategoryForm
from flask_login import current_user
from .... import db
from . import bp

@bp.route("/")
def list():
    categories = LinkdumpCategory.query.order_by(LinkdumpCategory.id.desc()).all()
    navigation = [
        {'text': _('Add category'), 'link': url_for('.category')}    
    ]
    data = dict(title=_("Categories list"), categories=categories, navigation=navigation)
    return render_template('admin/linkdump_categories/list.html', **data)
 
@bp.route("/category/<int:id>", methods=["GET", "POST"])   
@bp.route('/category', defaults={'id': None}, methods=["GET", "POST"])
def category(id):
    category = LinkdumpCategory() if id is None else LinkdumpCategory.query.get_or_404(id)
    form = CategoryForm()
    if form.is_submitted():
        if form.validate():
            category.name = form.name.data
            category.integrated_with_template = True if form.integrated_with_template.data else False
            category.lang_code = form.lang_code.data
            category.creator = current_user._get_current_object()
            
            db.session.add(category)
            db.session.commit()
            flash(_("Category added successfully."), category="success")
            return redirect(url_for('.list'))
    else:
        form = CategoryForm(obj=category)     
     
    navigation = []
    if category.id:
        navigation.append(
            {'text': _('Category links'), 'link': url_for('admin.linkdumps.list', category_id=category.id)}
        )
        
    navigation.append(       
        {'text': _('Categories list'), 'link': url_for('.list')}    
    )
    
    if category.id is None:
        form.lang_code.data = current_user.lang_code
        
    title = _("Add new category") if not category.id else _("Edit category")       
    data = dict(title=title, form=form, navigation=navigation)
    return render_template('admin/linkdump_categories/add.html', **data)
    
@bp.route("/delete/<int:id>")
def delete(id):
     category = LinkdumpCategory.query.get_or_404(id)
     if category.links.count():
         flash(_("Category have links. Can not be deleted."), category="danger")
         return redirect(url_for('.list'))
         
     db.session.delete(category)
     db.session.commit()
     flash(_("Category deleted successfully."), category="success")
     return redirect(url_for('.list'))  
