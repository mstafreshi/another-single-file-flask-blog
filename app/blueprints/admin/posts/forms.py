from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_babel import lazy_gettext as _l
from flask import current_app, g
from ....models import Story

class PostForm(FlaskForm):
    slug = StringField(_l("Slug"), validators=[DataRequired(), Length(1, 255)])
    title = StringField(_l("Title"), validators=[DataRequired()])
    active = BooleanField(_l("Active"))
    show_in_list = BooleanField(_l("Show in list?"))
    get_comment = BooleanField(_l("Get comment"))
    lang_code = SelectField(_l("Language"), validators=[DataRequired()])
    resume = TextAreaField(_l("Resume"), validators=[DataRequired()])
    body = TextAreaField(_l("Body"), validators=[DataRequired()], \
        description=_l("Some markdown tags are enabled"))        
    tags = StringField(_l("Tags"))
    story_id = SelectField(_l("Story"), coerce=int)
    meta_keywords = TextAreaField(_l("Meta keywords"))
    meta_description = TextAreaField(_l("Meta description"))    
    submit = SubmitField(_l("Submit"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lang_code.choices=[(lang, lang) for lang in current_app.config.get('LANG_CODES')]
        
        self.story_id.choices = [(0, "")] + [(story.id, story.name) for story in Story.query.filter_by(lang_code=self.lang_code.data).all()]
    
    def validate_story_id(self, field):
        if field.data:
            story = Story.query.get(int(field.data))
            if story is None or story.lang_code != self.lang_code.data:
                raise ValidationError()
            
    def validate_lang_code(self, field):
        if field.data not in current_app.config.get('LANG_CODES'):
            raise ValidationError()
                        
