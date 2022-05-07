from ast import Sub
from locale import currency
from tokenize import String
from turtle import title
from typing import Text
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, FloatField, IntegerField, TextAreaField, Form, FormField, FieldList
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskrecipe.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username',
        validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
        validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()     
        if user:
            raise ValidationError('Username has been taken already. Choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()     
        if user:
            raise ValidationError('Email has been used already. Choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
        validators=[DataRequired()])
    password = PasswordField('Password', 
        validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
        validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()     
            if user:
                raise ValidationError('Username has been taken already. Choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()     
            if user:
                raise ValidationError('Email has been used already. Choose a different one.')


class IngredientForm(Form):
    ingredient = TextAreaField('Ingredient', validators=[DataRequired()])
    quantity = FloatField('Quantity', validators=[DataRequired()])
    quantity_label = StringField('Label', validators=[DataRequired(), Length(min=0, max=15)])


class StepForm(Form):
    step = TextAreaField('Step', validators=[DataRequired()])


class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    time = IntegerField('Time in Minutes', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    ingredients = FieldList(FormField(IngredientForm), label='Ingredients', min_entries=1,max_entries=20)
    steps = FieldList(FormField(StepForm), label='Steps', min_entries=1, max_entries=15)

    submit = SubmitField('Create')