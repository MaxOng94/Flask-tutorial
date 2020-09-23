from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed       # for flask to upload files (in our case we want image extensions file). FileAllowed --> restrict to .jpg or .png
from wtforms import StringField, PasswordField, BooleanField,SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User
from flask_login import current_user

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

    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        # if user is none, the validationerror will not be raised
        if user:
            raise ValidationError("That username is taken. Please choose a different one.")


    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        # if user is none, the validationerror will not be raised
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")


class LoginForm(FlaskForm):
    # validators : list of validators we want in our username --> eg: not leave it empty, cannot be more than 20 chars long etc

    email = StringField("Email",
                        validators = [DataRequired(), Email()])

    password = PasswordField("Password",
                             validators= [DataRequired()])
    # allows user to stay login sometime after their browser closes using a secure cookie
    remember = BooleanField("Remember Me")

    submit = SubmitField("Login")



class UpdateAccountForm(FlaskForm):
    # validators : list of validators we want in our username --> eg: not leave it empty, cannot be more than 20 chars long etc
    username = StringField("Username", # label
                            validators= [DataRequired(), Length(min = 2, max = 20)])

    email = StringField("Email",
                        validators = [DataRequired(), Email()])
    picture = FileField("Update Profile Picture",
                        validators = [FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Update")


    def validate_username(self,username):
        if username.data != current_user.username:  # only if the new username (username.data) is different from the existing username,
            user = User.query.filter_by(username = username.data).first()  #then we check the database if the new username is already used before.

            # if user is none, the validationerror will not be raised
            if user:
                raise ValidationError("That username is taken. Please choose a different one.")


    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            # if user is none, the validationerror will not be raised
            if user:
                raise ValidationError("That email is taken. Please choose a different one.")
