from flask import render_template, redirect, url_for, flash, abort, request, current_app, g
from flask_login import current_user, login_required
from flask_babel import _
from sqlalchemy import desc
from . import bp
from ....models import Post, Comment, User, LinkdumpCategory, Tag
from .forms import CommentForm
from ...admin.users.forms import EditForm as UserProfileForm
from .... import db
import urllib.parse

# lang_code view arg is now in g.lang_code

@bp.context_processor
def context_processor():
    authors = User.query.join(Post.author).filter(Post.lang_code==g.lang_code)
    tags = Tag.query.join(Tag.posts).filter_by(lang_code=g.lang_code)
    return dict(LinkdumpCategory=LinkdumpCategory, tags=tags, authors=authors)
               
@bp.route("/", defaults={'lang_code': None, 'page':1})
@bp.route("/<lang_code>", defaults={'page':1})
@bp.route("/<lang_code>/<int:page>")
def index(lang_code, page):
    pagination = Post.query.filter_by(active = True) \
        .filter_by(show_in_list = True, lang_code=g.lang_code) \
        .order_by(desc(Post.id)).paginate(page=page, per_page=10, error_out=False)
    posts = pagination.items
    data = dict(title=_("Home"), posts=posts, pagination=pagination)
    return render_template('user/index/index.html', **data)

@bp.route('/<lang_code>/tag/<tag>', defaults={'page':1})
@bp.route('/<lang_code>/tag/<tag>/<int:page>')
def tag(lang_code, tag, page):
    # in development server is not necessary but in deploy yes
    # Must change
    tag = urllib.parse.unquote(tag)
    tag_object = Tag.query.filter_by(name=tag).first_or_404()
    pagination = tag_object.posts.filter_by(lang_code=g.lang_code, \
        show_in_list=True,active=True)\
        .order_by(Post.id.desc()).paginate(page=page, per_page=10, error_out=False)                          
    posts = pagination.items
    print(posts)
    data = dict(title=tag, tag=tag, posts=posts, pagination=pagination)
    return render_template('user/index/index.html', **data)        

@bp.route("/<lang_code>/author/<username>", defaults={'page':1})
@bp.route("/<lang_code>/author/<username>/<int:page>")
def author(lang_code, username, page):
    user = User.query.filter_by(username=username).one_or_404()    
    pagination = user.posts.filter_by(active = True, lang_code=g.lang_code) \
        .order_by(Post.id.desc()).paginate(page=page, per_page=10, error_out=False)
    posts = pagination.items
    data = dict(title=_("Posts of") + " " + user.name, posts=posts, pagination=pagination, author=user)
    return render_template('user/index/index.html', **data)
        
@bp.route("/<lang_code>/post/<slug>", methods=["GET", "POST"])
def post(lang_code, slug):
    post = Post.query.filter_by(lang_code=g.lang_code, slug=slug).first_or_404(id)   
    if not post.active:
        abort(404)     
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
    # todo: I pass Post and Comment Class to template just for 
    # use them in order_by method!
    return render_template('user/index/profile.html', user=user, Post=Post, Comment=Comment)

@bp.route("/<lang_code>/edit_profile/<username>", methods=["GET", "POST"])
@login_required
def edit_profile(lang_code, username):
    title = _("Edit Profile")
    form = UserProfileForm()
    del form.active
    
    if form.is_submitted():
        if form.validate():
            cu = current_user._get_current_object()
            cu.name = form.name.data.strip()
            cu.email = form.email.data.strip()
            cu.twitter = form.twitter.data.strip()
            cu.facebook = form.facebook.data.strip()
            cu.linkedin = form.linkedin.data.strip()
            cu.github = form.github.data.strip()
            cu.instagram = form.instagram.data.strip()
            cu.youtube = form.youtube.data.strip()        
            cu.about = form.about.data.strip()
            cu.lang_code = form.lang_code.data
            
            db.session.add(cu)
            db.session.commit()
            
            flash(_("Profile saved seccessfully"), category="success")
                
            return redirect(url_for('user.index.edit_profile', lang_code=g.lang_code, \
                username=current_user.username))
    else:                                
        form = UserProfileForm(obj=current_user)
        del form.active
                          
    return render_template("user/index/edit_profile.html", title=title, form=form)
