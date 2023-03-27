from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, PasswordField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_babel import lazy_gettext as _l

class EditForm(FlaskForm):
    name = StringField(_l("Name"), validators=[DataRequired()])
    email = StringField(_l("Email"), validators=[DataRequired(), Email()])    
    twitter = StringField(_l("Twitter account"))
    facebook = StringField(_l("Facebook account"))
    linkedin = StringField(_l("Linkedin account"))
    instagram = StringField(_l("Instagram account"))
    github = StringField(_l("Github account"))
    youtube = StringField(_l("Youtube account"))
    image = FileField(_l("Profile image"))
    about = TextAreaField(_l("About"))
    lang_code = SelectField(_l("Language"), coerce=str, validators=[DataRequired()],
                    description = _l("Admin panel will be shown in this language"))                                
    active = BooleanField(_l("Active"))    
    submit = SubmitField(_l("Edit"))  
    
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
    password = PasswordField(_l("Password"), validators=[DataRequired(), EqualTo('confirm_password', message=_l("Password must match with Confirm password"))])
    confirm_password = PasswordField(_l("Confirm password"), validators=[DataRequired()])
    submit = SubmitField(_l("Edit"))
