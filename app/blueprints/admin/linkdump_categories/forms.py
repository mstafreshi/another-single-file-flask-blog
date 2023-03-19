from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, ValidationError

class CategoryForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    lang_code = SelectField("Language", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lang_code.choices = [(lang, lang) for lang in current_app.config.get('LANG_CODES')]
        
    def validate_lang_code(self, field):
        if field.data not in current_app.config.get('LANG_CODES'):
            validationError()    