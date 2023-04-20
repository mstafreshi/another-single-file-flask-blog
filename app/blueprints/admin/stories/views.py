from flask import render_template, g, flash, url_for, redirect
from flask_babel import _
from .forms import StoryForm
from ....models import Story
from .... import db
from . import bp

@bp.route("/list")
def list():
    stories = Story.query.order_by(Story.id.desc()).all()
    navigation = [
        {
            'text': _('Add story'),
            'link': url_for('.story')
        }    
    ]
    return render_template("admin/stories/list.html", stories=stories, navigation=navigation)
    
@bp.route("/story", methods=["GET", "POST"], defaults={'id':None})
@bp.route("/story/<int:id>", methods=["GET", "POST"])
def story(id):
    if id is None:
        story = Story()
    else:
        story = Story.query.get_or_404(id)
        
    form = StoryForm()
    if form.is_submitted():
        if form.validate():
            story.name = form.name.data.strip()
            story.lang_code = form.lang_code.data
            
            db.session.add(story)
            db.session.commit()
            
            flash(_("Story added successfully"), category="success")
            return redirect(url_for('.list'))
            
    form = StoryForm(obj=story)
    
    navigation = [
        {
            'text': _('Back to') + " " + _('Stories'),
            'link': url_for('.list')
        }    
    ]
    
    title = _('Edit story') if story.id else _('Add story')             
    data=dict(title=title, form=form, navigation=navigation, story=story)
    return render_template("admin/stories/story.html", **data)
    
@bp.route("/delete/<int:id>")
def delete(id):
    story = Story.query.get_or_404(id)
    if story.posts.count():
        flash(_("This story has posts and cannot be deleted"), category="danger")
        return redirect(url_for('.list'))
        
    db.session.delete(story)
    db.session.commit()
    
    flash(_("Story deleted successfully."), category="success")
    return redirect(url_for('.list')) 
