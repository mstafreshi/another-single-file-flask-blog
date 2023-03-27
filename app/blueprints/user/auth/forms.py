from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError
from ....models import User

class LoginForm(FlaskForm):
    username = StringField(_l("Username"), validators=[DataRequired()])
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    remember_me = BooleanField(_l("Remember me"))
    submitField = SubmitField(_l("Login"))
    
class RegisterForm(FlaskForm):
    name = StringField(_l("Name"), validators=[DataRequired()])
    email = StringField(_l("Email"), validators=[DataRequired(), Email(), Length(1, 64)])
    username = StringField(_l("Username"), validators=[DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, _l('Uername must have only letters, '
            'numbers, dots or underscores'))])
    password = PasswordField(_l("Password"), validators=[DataRequired(), EqualTo('confirm_password', message=_l('Password must match with Confirm password'))])
    confirm_password = PasswordField(_l("Confirm password"), validators=[DataRequired()])
    submit = SubmitField(_l("Register"))
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(_l("Email already exists."))
            
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(_l("Username have been taken."))            
