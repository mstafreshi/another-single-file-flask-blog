from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.mysql import LONGTEXT
from . import login_manager
from . import db
from datetime import datetime
from markdown import markdown
from hashlib import md5

class AnonymousUser(AnonymousUserMixin):
    def get_lang_code(self):
        return current_app.config.get('DEFAULT_LANG_CODE')
        
    def can(self, permissions):
        return False
        
    def is_administrator(self):
        return False                
        
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    twitter = db.Column(db.String(64))
    facebook = db.Column(db.String(64))
    linkedin = db.Column(db.String(64))
    instagram = db.Column(db.String(64))
    github = db.Column(db.String(64))
    youtube = db.Column(db.String(64)) 
    image = db.Column(db.String(128))
    about = db.Column(db.Text)
    about_html = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)
    lang_code = db.Column(db.String(2))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    linkdump_categories = db.relationship('LinkdumpCategory', backref='creator', lazy='dynamic')
    linkdumps = db.relationship('Linkdump', backref='creator', lazy='dynamic')
    
    @staticmethod
    def on_changed_about(target, value, oldvalue, initiator):
        target.about_html = markdown(value, output_format='html', 
            extensions=[
                'pymdownx.emoji',
                'pymdownx.mark',
                'pymdownx.keys',
                'extra', 
                'codehilite', 
                'admonition', 
                'toc'
            ]
        )
        
    def avatar(self, size):
        if self.image:
            return self.image
            
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions
            
    def is_administrator(self):
        return self.can(Permission.ADMINISTRATOR)
                    
    def get_lang_code(self):
        return self.lang_code or current_app.config.get('DEFAULT_LANG_CODE')
               
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
        
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

posts_tags = db.Table('posts_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True,index=True)
    posts = db.relationship('Post', secondary=posts_tags, backref=db.backref('tags', lazy='dynamic'), lazy='dynamic')

class Story(db.Model):
    __tablename__ = 'stories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    lang_code = db.Column(db.String(2))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='story', lazy='dynamic')
        
class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(255))
    lang_code = db.Column(db.String(2))
    resume = db.Column(db.Text, nullable=False)
    resume_html = db.Column(db.Text)
    body = db.Column(LONGTEXT, nullable=False)
    body_html = db.Column(LONGTEXT)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    active = db.Column(db.Boolean, default = False)
    get_comment = db.Column(db.Boolean, default=True)
    show_in_list = db.Column(db.Boolean, default=True)
    image = db.Column(db.String(128))
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'), index=True, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    meta_keywords = db.Column(db.String(500))
    meta_description = db.Column(db.String(500))
    last_edit_note = db.Column(db.String(500))
    
    @staticmethod
    def on_changed_body_or_resume(target, value, oldvalue, initiator):
        md = markdown(value, output_format='html', 
            extensions=[
                'pymdownx.emoji',
                'pymdownx.mark',
                'pymdownx.keys',
                'extra', 
                'codehilite', 
                'admonition', 
                'toc'
            ]
        )
        
        if initiator.key == 'body':
            target.body_html = md
        elif initiator.key == 'resume':
            target.resume_html = md            
                               
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    comment = db.Column(db.Text(), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))       
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    children = db.relationship('Comment')
    
    def avatar(self, size):
        if self.author:
            return self.author.avatar(size)
            
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
class LinkdumpCategory(db.Model):
    __tablename__ = 'linkdump_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    lang_code = db.Column(db.String(2))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    links = db.relationship('Linkdump', backref='category', lazy='dynamic')
    
class Linkdump(db.Model):
    __tablename__ = 'linkdumps'
    id = db.Column(db.Integer, primary_key=True)    
    text = db.Column(db.String(255))
    alt = db.Column(db.String(255))
    link = db.Column(db.String(500))
    linkdump_category_id = db.Column(db.Integer, db.ForeignKey('linkdump_categories.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    permissions = db.Column(db.Integer, default=0x00)
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    @staticmethod
    def write_roles():
        roles = {
            'Registered_user': 0x0000,
            'Administrator': 0xffff,      
        }
        
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r]
            db.session.add(role)
        db.session.commit()
                   
class Permission:
    ADMINISTRATOR = 0x8000
    
db.event.listen(Post.body, 'set', Post.on_changed_body_or_resume)
db.event.listen(Post.resume, 'set', Post.on_changed_body_or_resume)
db.event.listen(User.about, 'set', User.on_changed_about)
   
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
login_manager.anonymous_user = AnonymousUser
