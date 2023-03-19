from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, PasswordField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

class EditForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])    
    twitter = StringField("Twitter account")
    facebook = StringField("Facebook account")
    linkedin = StringField("Linkedin account")
    instagram = StringField("Instagram account")
    github = StringField("Github account")
    youtube = StringField("Youtube account")
    image = FileField("Profile image")
    about = TextAreaField("About")
    lang_code = SelectField("Language", coerce=str, validators=[DataRequired()],
                    description = "Admin panel will be shown in this language")                                
    active = BooleanField("Active")    
    submit = SubmitField("Edit")  
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lang_code.choices = [(lang, lang) for lang in current_app.config.get('LANG_CODES')]
    
    def validate_lang_code(self, field):
        if field.data not in current_app.config.get('LANG_CODES'):
            raise ValidationError()
                
    def fill_data(self, obj):
        obj.name = self.name.data.strip()
        obj.active = self.active.data
        obj.email = self.email.data.strip()
        obj.twitter = self.twitter.data.strip()
        obj.facebook = self.facebook.data.strip()
        obj.linkedin = self.linkedin.data.strip()
        obj.github = self.github.data.strip()
        obj.instagram = self.instagram.data.strip()
        obj.youtube = self.youtube.data.strip()        
        obj.about = self.about.data.strip()
        obj.lang_code = self.lang_code.data
            
class PasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('confirm_password', message="Password must match with Confirm Password")])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Edit")