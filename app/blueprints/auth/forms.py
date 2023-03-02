from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError
from ...models import User

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submitField = SubmitField("Login")
    
class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(1, 64)])
    username = StringField("Username", validators=[DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Uername must have only letters, '
            'numbers, dots or underscores')])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('confirm_password', message='Password must match with Confirm password')])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Register")
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already exists.")
            
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username have been taken.")            
