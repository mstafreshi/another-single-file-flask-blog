from flask import render_template, flash, redirect, url_for, request
from flask_babel import _
from ....models import Comment, Post
from .... import db
from . import bp

@bp.route("/list", defaults={'id': None})
@bp.route("/list/<int:id>")
def list(id):
    if id is None:
        comments = Comment.query.filter_by(active=False)
    else:
        post = Post.query.get_or_404(id)
        comments = post.comments
    
    title = _("Not approved comments") if id is None else _("Manage comments of \"") + post.title + "\""
    navigation = [
        {'text': _('Back to posts'), 'link': url_for('admin.posts.list') }
    ]
    data = dict(title=title , comments=comments, post_id=id, navigation=navigation);
    return render_template('admin/comments/list.html', **data)

@bp.route('/delete_comment/<int:id>')
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    post_id = comment.post.id
    
    db.session.delete(comment)
    db.session.commit()
    
    flash(_("Comment deleted successfully"), category="success")
    return redirect(url_for('.list', id=post_id))
    
    
@bp.route('/active_comment/<int:id>')
def active_comment(id):
    back_to_post = request.args.get('back_to_post')
  
    comment = Comment.query.get_or_404(id)
    if comment.active:
        redirect(url_for('.list'))
        
    comment.active = True
    db.session.add(comment)
    db.session.commit()
    
    flash(_("Comment acivated successfully"), category="success")
    return redirect(url_for('.list', id=comment.post.id if back_to_post == "ok" else None))

@bp.route('/deactive_comment/<int:id>')
def deactive_comment(id):
    back_to_post = request.args.get('back_to_post')
  
    comment = Comment.query.get_or_404(id)
    if not comment.active:
        redirect(url_for('.list'))
        
    comment.active = False
    db.session.add(comment)
    db.session.commit()
    
    flash(_("Comment deacivated successfully"), category="success")
    return redirect(url_for('.list', id=comment.post.id if back_to_post == "ok" else None))   
