from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from food_app.constants import units_of_measure
from food_app.models import User, Product, Recipe


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ShoppingListForm(FlaskForm):
    title = StringField('Title')
    submit = SubmitField('Create')


class AddProductForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    type_of_product = SelectField('Type of Product', choices=[
            ('other', 'other'),
            ('fruit', 'fruit'),
            ('vegetable', 'vegetable'),
            ('meet', 'meet'),
            ('fish', 'fish'),
            ('milk', 'milk'),
            ('grain', 'grain'),
            ('sweets', 'sweets'),
            ('spice and souse', 'spice and souse'),
            ('beverage', 'beverage'),
        ])
    unit_of_measure = SelectField('Unit of Measure', choices=units_of_measure)
    submit = SubmitField('   Add   ')


    def validate_title(self, title):
        product = Product.query.filter_by(title=title.data).first()
        if product is not None:
            raise ValidationError('This title already exists.')


class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    ingredients = StringField('Ingredients')
    description = TextField('Description')
    submit = SubmitField('   Add   ')

    def validate_title(self, title):
        recipe = Recipe.query.filter_by(title=title.data).first()
        if recipe is not None:
            raise ValidationError('This title already exists.')





# class ShoppingListItemForm(FlaskForm):