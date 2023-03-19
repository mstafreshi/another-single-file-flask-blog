from flask import render_template, redirect, url_for, flash, abort, request, current_app, g
from flask_login import current_user
from flask_babel import _
from sqlalchemy import desc
from . import bp
from ....models import Post, Comment, User, LinkdumpCategory
from .forms import CommentForm
from .... import db

@bp.context_processor
def context_processor():
    return dict(LinkdumpCategory=LinkdumpCategory)
        
@bp.route("/", defaults={'lang_code': None})
@bp.route("/<lang_code>")
def index(lang_code):
    if lang_code is None:
        lang_code = current_app.config.get('DEFAULT_LANG_CODE')
           
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(active = True) \
        .filter_by(show_in_list = True, lang_code=lang_code) \
        .order_by(desc(Post.id)).paginate(page=page, per_page=20, error_out=False)
    posts = pagination.items
    g.lang_code = lang_code         
    data = dict(title=_("Home"), posts=posts, pagination=pagination, page=page)
    return render_template('user/index/index.html', **data)
    
@bp.route("/<lang_code>/post/<slug>", methods=["GET", "POST"])
def post(lang_code, slug):
    post = Post.query.filter_by(lang_code=lang_code, slug=slug).first_or_404(id)   
    if not post.active:
        abort(404)
    g.lang_code=post.lang_code   
    comment_form = CommentForm()
    if current_user.is_authenticated:
        del comment_form.name
        del comment_form.email
        
    if comment_form.validate_on_submit():      
        comment = Comment()
        comment.post = post
        
        if comment_form.parent_id.data:
            post.comments.filter_by(id = int(comment_form.parent_id.data)).first_or_404()
            comment.parent_id = int(comment_form.parent_id.data)

        if current_user.is_authenticated:
            comment.author = current_user._get_current_object()
        else:
            comment.name = comment_form.name.data.strip()
            comment.email = comment_form.email.data.strip()
        
        comment.comment = comment_form.comment.data.strip()            
        
        db.session.add(comment)
        db.session.commit()
        
        flash(_("Comment saved successfully"), category = "success")
        return redirect(url_for('.post', lang_code=post.lang_code, slug=post.slug))
        
    data = dict(title=post.title, post=post, comment_form=comment_form)
    return render_template("user/index/post.html", **data)
    
@bp.route("/<lang_code>/profile/<username>")    
def profile(lang_code, username):       
    user = User.query.filter_by(username=username, active=True).first_or_404()
    g.lang_code = lang_code
    return render_template('user/index/profile.html', user=user)
    
@bp.route("/<lang_code>/edit_profile/<username>")
def edit_profile():
    pass