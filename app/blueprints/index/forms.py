from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

class CommentForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[Email()])
    comment = TextAreaField("comment", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
    def fill_data(self, obj):
        obj.name = self.name.data.strip()
        obj.email = self.email.data.strip()
        obj.comment = self.comment.data.strip()
