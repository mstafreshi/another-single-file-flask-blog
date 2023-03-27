from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email
from flask_babel import lazy_gettext as _l
class CommentForm(FlaskForm):
    parent_id = HiddenField()
    name = StringField(_l("Name"), validators=[DataRequired()])
    email = StringField(_l("Email"), validators=[Email()])
    comment = TextAreaField(_l("comment"), validators=[DataRequired()])
    submit = SubmitField(_l("Submit"))