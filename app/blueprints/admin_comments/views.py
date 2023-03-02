from flask import render_template, flash, redirect, url_for, request
from ...models import Comment, Post
from ... import db
from . import admin_comments as bp

@bp.route("/list", defaults={'id': None})
@bp.route("/list/<int:id>")
def list(id):
    if id is None:
        comments = Comment.query.filter_by(active=False).all()
    else:
        post = Post.query.get_or_404(id)
        comments = post.comments
        
    data = dict(title="Manage comments", comments=comments, post_id=id);
    return render_template('admin_comments/list.html', **data)

@bp.route('/delete_comment/<int:id>')
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    post_id = comment.post.id
    
    db.session.delete(comment)
    db.session.commit()
    
    flash("Comment deleted successfully", category="success")
    return redirect(url_for('admin_comments.list', id=post_id))
    
    
@bp.route('/active_comment/<int:id>')
def active_comment(id):
    back_to_post = request.args.get('back_to_post')
  
    comment = Comment.query.get_or_404(id)
    if comment.active:
        redirect(url_for('admin_comments.list'))
        
    comment.active = True
    db.session.add(comment)
    db.session.commit()
    
    flash("Comment acivated successfully", category="success")
    return redirect(url_for('admin_comments.list', id=comment.post.id if back_to_post == "ok" else None))
   
