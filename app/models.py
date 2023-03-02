from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from . import db
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    image = db.Column(db.String(128))
    about = db.Column(db.String(500))
    active = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='user')
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
        
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
        
class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    resume = db.Column(db.String(500), nullable=False)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    active = db.Column(db.Boolean, default = False)
    show_in_list = db.Column(db.Boolean, default=True)
    image = db.Column(db.String(128))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='post')
    
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64))
    comment = db.Column(db.Text(), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False, index=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
  
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
