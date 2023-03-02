from flask import render_template, redirect, url_for, flash, abort
from sqlalchemy import desc
from . import index as bp
from ...models import Post, Comment
from .forms import CommentForm
from ... import db

@bp.route("/")
def index():
    posts = Post.query.filter_by(active = True).filter_by(show_in_list = True).order_by(desc(Post.id)).all()
    data = dict(title="index", posts=posts)
    return render_template('index/index.html', **data)
    
@bp.route("/post/<int:id>", methods=["GET", "POST"])
def post(id):
    post = Post.query.get_or_404(id)
    if not post.active:
        abort(404)
        
    comment_form = CommentForm()
    
    if comment_form.validate_on_submit():
        comment = Comment()
        comment_form.fill_data(comment)
        comment.post_id = post.id
        db.session.add(comment)
        db.session.commit()
        
        flash("Comment saved successfully", category = "success")
        return redirect(url_for('index.post', id=post.id))
        
    data = dict(title=post.title, post=post, comment_form=comment_form)
    return render_template("index/post.html", **data)
