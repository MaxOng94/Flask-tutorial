from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

# class for registration form. We can inherit from FlaskForm class from flask_wtf
class RegistrationForm(FlaskForm):
    # validators : list of validators we want in our username --> eg: not leave it empty, cannot be more than 20 chars long etc
    username = StringField("Username", # label
                            validators= [DataRequired(), Length(min = 2, max = 20)])

    email = StringField("Email",
                        validators = [DataRequired(), Email()])

    password = PasswordField("Password",
                             validators= [DataRequired()])

    confirm_password = PasswordField("Confirm Password",
                                     validators= [DataRequired(),EqualTo('password')])

    submit = SubmitField("Sign up")


class LoginForm(FlaskForm):
    # validators : list of validators we want in our username --> eg: not leave it empty, cannot be more than 20 chars long etc

    email = StringField("Email",
                        validators = [DataRequired(), Email()])

    password = PasswordField("Password",
                             validators= [DataRequired()])
    # allows user to stay login sometime after their browser closes using a secure cookie
    remember = BooleanField("Remember Me")

    submit = SubmitField("Login")
