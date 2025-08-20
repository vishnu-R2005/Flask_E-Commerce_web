from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, FloatField, BooleanField, EmailField
from wtforms.validators import InputRequired, Length, Email, EqualTo


# ✅ Registration Form (with confirm password)
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=50)])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


# ✅ Login Form
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# ✅ Product Form (for Admin to add products)
class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[InputRequired()])
    price = FloatField('Price', validators=[InputRequired()])
    description = StringField('Description')
    image = FileField('Product Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Add Product')


# ✅ Update Profile Form (for user profile updates)
class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=50)])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    profile_image = FileField('Profile Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Update Profile')
