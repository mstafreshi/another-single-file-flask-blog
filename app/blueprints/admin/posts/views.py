from flask import render_template, redirect, flash, url_for, abort, request, g
from flask_babel import _
from flask_login import current_user
from flask_babel import get_locale
from sqlalchemy import desc
from .forms import PostForm
from ....models import Post, Comment, Tag
from .... import db
from . import bp

@bp.route("/list")
def list():
    posts = Post.query.order_by(desc(Post.id)).all()
    navigation = [
        {'text': _('Add new post'), 'link': url_for('.post') }
    ]
    data = dict(title=_("Posts list"), posts=posts, navigation=navigation)
    return render_template('admin/posts/list.html', **data)
 
@bp.route("/post/<int:id>", methods=["GET", "POST"])
@bp.route("/post", defaults={'id': None}, methods=["GET", "POST"])
def post(id):
    post = Post() if id is None else Post.query.get_or_404(id)
    form = PostForm()    
    if form.is_submitted():    
        if form.validate():
            post.title = form.title.data
            post.slug = form.slug.data
            post.resume = form.resume.data
            post.body = form.body.data
            post.active = form.active.data
            post.show_in_list = form.show_in_list.data
            post.get_comment = form.get_comment.data        
            post.author = current_user._get_current_object() 
            post.lang_code = form.lang_code.data
            
            for post_tag in post.tags.all():
                post.tags.remove(post_tag)
            
            for tag in form.tags.data.split('+'):
                tag = tag.strip()
                if not tag:
                    continue                      
                tag_obj = Tag.query.filter_by(name=tag).first()
                if tag_obj:
                    if tag_obj in post.tags:
                        continue
                else:
                    tag_obj = Tag(name=tag.strip())
                post.tags.append(tag_obj)
                    
            db.session.add(post)
            db.session.commit()
        
            flash(_('Post added/editted successfuly'), category='success')
            return redirect(url_for('.post', id=post.id))
    else:
        form = PostForm(obj=post)
               
    form.tags.data = "+".join([tag.name for tag in post.tags.all()])       
    if not post.id:
        form.lang_code.data = current_user.lang_code
        
    navigation = [
        {'text': _("See"), 'link': url_for('user.index.post', \
            lang_code=post.lang_code, slug=post.slug)},
        {'text': _('Comments') + ' <span class="badge bg-danger">' + \
            str(post.comments.count()) + '</span>', \
            'link': url_for('admin.comments.list', id=post.id)},
        {'text': _('Back to posts'), 'link': url_for('.list') }
    ]
    
    title = _("Edit post") if id else _("Add post")
    data = dict(title=title, form=form, navigation=navigation)
    return render_template('admin/posts/post.html', **data)
