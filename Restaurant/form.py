from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from Restaurant.model import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken. Please choose a different one.")
        
    def validate_email(self, email):    
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is already in use. Please choose a different one or login with it.")


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# class reserve(FlaskForm):
#     name=StringField('Email',
#                         validators=[DataRequired(), Email()])
#     phoneno=StringField('Phone Number',validators=[DataRequired(),Length(min=10,max=10)])
#     seats=StringField('Seats',validators=[DataRequired(),Length(min=1,max=20)])
#     DateandTime=StringField('DateandTime',validators=[DataRequired()])
