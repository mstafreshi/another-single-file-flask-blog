from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_babel import lazy_gettext as _l
from flask_pagedown.fields import PageDownField
from flask import current_app

class PostForm(FlaskForm):
    slug = StringField(_l("Slug"), validators=[DataRequired(), Length(1, 255)])
    title = StringField(_l("Title"), validators=[DataRequired()])
    active = BooleanField(_l("Active"))
    show_in_list = BooleanField(_l("Show in list?"))
    get_comment = BooleanField(_l("Get comment"))
    lang_code = SelectField(_l("Language"), validators=[DataRequired()])
    resume = TextAreaField(_l("Resume"), validators=[DataRequired()])
    body = PageDownField(_l("Body"), validators=[DataRequired()], \
        description=_l("Some markdown tags are enabled"))        
    tags = StringField(_l("Tags"))
    submit = SubmitField(_l("Submit"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lang_code.choices=[(lang, lang) for lang in current_app.config.get('LANG_CODES')]
        
    def validate_lang_code(self, field):
        if field.data not in current_app.config.get('LANG_CODES'):
            raise ValidationError()