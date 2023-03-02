from flask import render_template, redirect, flash, url_for, abort, request
from flask_login import current_user
from . import admin_posts as bp
from sqlalchemy import desc
from .forms import PostForm
from ...models import Post, Comment
from ... import db

@bp.before_request
def security_checks():
    if not current_user.is_authenticated:
        abort(403)
        
@bp.route("/list")
def list():
    posts = Post.query.order_by(desc(Post.id)).all()
    data = dict(title="Post list", posts=posts)
    return render_template('admin_posts/list.html', **data)
 
@bp.route("/post/<int:id>", methods=["GET", "POST"])
@bp.route("/post", defaults={'id': None}, methods=["GET", "POST"])
def post(id):
    post = Post() if id is None else Post.query.get_or_404(id)
    form = PostForm()    
    if form.is_submitted():    
        if form.validate():
            post.title = form.title.data
            post.resume = form.resume.data
            post.body = form.body.data
            post.active = form.active.data
            post.show_in_list = form.show_in_list.data
            # this must be fixed
            post.user_id = 1        
            db.session.add(post)
            db.session.commit()
        
            flash('Post added/editted successfuly', category='success')
            return redirect(url_for('.post', id=post.id))
    else:
        form = PostForm(obj=post)
        
    title = "Edit post" if id else "Add post"
    data = dict(title=title, form=form)
    return render_template('admin_posts/post.html', **data)
