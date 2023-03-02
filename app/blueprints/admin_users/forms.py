from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class EditForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])    
    about = TextAreaField("About")    
    submit = SubmitField("Edit")
    
    def fill_data(self, obj):
        obj.name = self.name.data
        obj.about = self.about.data
    
class EditEmailForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Edit")
    
    def fill_data(self, obj):
        obj.email = self.email.data
    
class EditPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('confirm_password', message="Password must match with Confirm Password")])
    confirm_password = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField("Edit")
    
    def fill_data(self, obj):
        obj.password = self.password.data
    
class EditStatusForm(FlaskForm):
    active = BooleanField("Active")
    submit = SubmitField("Edit")
    
    def fill_data(self, obj):
        obj.active = self.active.data
