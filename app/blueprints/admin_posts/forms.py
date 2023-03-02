from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    resume = TextAreaField("Info", validators=[DataRequired()])
    body = TextAreaField("Body")
    active = BooleanField("active")
    show_in_list = BooleanField("Show this post in list")
    submit = SubmitField("Submit")
