from flask import current_app
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError

class StoryForm(FlaskForm):
    name = StringField(_l("Name"), validators=[DataRequired()])
    lang_code = SelectField(_l("Language"), validators=[DataRequired()])
    submit = SubmitField(_l("Submit"))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lang_code.choices = [(lang, lang) for lang in current_app.config.get('LANG_CODES')]
        
    def validate_lang_code(self, field):
        if field.data not in current_app.config.get('LANG_CODES'):
            validationError()   
