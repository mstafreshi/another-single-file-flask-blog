from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class LinkForm(FlaskForm):
    category = StringField("Category", render_kw={'disabled': True})
    text = StringField("Text", validators=[DataRequired()])
    alt = StringField("Alt text", validators=[DataRequired()])
    link = StringField("Link", validators=[DataRequired()])
    submit = SubmitField("Submit")