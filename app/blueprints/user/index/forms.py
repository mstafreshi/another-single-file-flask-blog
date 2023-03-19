from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email

class CommentForm(FlaskForm):
    parent_id = HiddenField()
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[Email()])
    comment = TextAreaField("comment", validators=[DataRequired()])
    submit = SubmitField("Submit")