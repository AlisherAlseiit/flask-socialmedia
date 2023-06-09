from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from .models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')
        
    def validate_email_address(self, email_to_check):
        email = User.query.filter_by(email_address=email_to_check.data).first()
        if email:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label="User Name:", validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label="Email:", validators=[Email(), DataRequired()])
    password = PasswordField(label="Password:", validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label="Confirm Password:", validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label="Create Account")


class LoginForm(FlaskForm):
    username = StringField(label="User Name:", validators=[Length(min=2, max=30), DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    submit = SubmitField(label="Sign In")


class PostForm(FlaskForm):
    title = StringField(label="Title: ", validators=[Length(max=30), DataRequired()])
    content = StringField(label="Content: ", validators=[DataRequired()])
    submit = SubmitField(label="Create Post")