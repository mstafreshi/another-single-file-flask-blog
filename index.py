from flask import Flask, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_migrate import Migrate
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KhodayeMan'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mohsen@localhost/mstafreshi'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
bootstrap = Bootstrap5(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route("/")
def index():
    data = dict(title="index")
    return render_template('es/index.html', **data)
    
    
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return 'hello world'
    
    data = dict(title="Login", form=form)    
    return render_template('es/login.html', **data)
    
@app.route("/register")
def register():
    data = dict(title="Register")
    return render_template('es/register.html', **data)        

@app.route("/posts-list")
def posts_list():
    posts = Post.query.order_by(desc(Post.id)).all()
    data = dict(title="Post list", posts=posts)
    return render_template('es/posts_list.html', **data)

@app.route("/post/<int:id>", methods=["GET", "POST"])
@app.route("/post", defaults={'id': None}, methods=["GET", "POST"])
def post(id):
    post = Post() if id is None else Post.query.get_or_404(id)   
    form = PostForm()
           
    if form.validate_on_submit():
        post.title = form.title.data
        post.info = form.info.data
        post.body = form.body.data
        # this must be fixed
        post.user_id = 1        
        db.session.add(post)
        db.session.commit()
        
        flash("Post added/editted successfuly")
        return redirect(url_for('post', id=post.id))
    
    form = PostForm(obj=post)      
    data = dict(title='Posts', form=form)
    return render_template('es/post.html', **data)

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    info = TextAreaField("Info", validators=[DataRequired()])
    body = TextAreaField("Body", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submitField = SubmitField("Login")
    
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password = db.Column(db.String(64), nullable=True)
    name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    posts = db.relationship('Post', backref='user')
    
class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    info = db.Column(db.String(500), nullable=False)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

