from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_babel import lazy_gettext as _l

class LinkForm(FlaskForm):
    category = StringField(_l("Category"), render_kw={'disabled': True})
    text = StringField(_l("Text"), validators=[DataRequired()])
    alt = StringField(_l("Alt text"), validators=[DataRequired()])
    link = StringField(_l("Link"), validators=[DataRequired()])
    submit = SubmitField(_l("Submit"))