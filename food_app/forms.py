from flask_login._compat import unicode
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, SelectField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from food_app.constants import units_of_measure
from food_app.models import User, Product, Recipe, ShoppingList


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
    submit = SubmitField('   Create   ')


class AddPortionsForm(FlaskForm):
    shopping_list_title = StringField('Shopping List Title')
    number_of_portions = SelectField('Number of Portions', choices=[
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
       ])
    submit = SubmitField('   Add Portions   ')


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


class AddRecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    ingredients = StringField('Ingredients')
    description = TextField('Description')
    submit = SubmitField('   Add   ')

    def validate_title(self, title):
        recipe = Recipe.query.filter_by(title=title.data).first()
        if recipe is not None:
            raise ValidationError('This title already exists.')


class NewShoppingListForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    notes = TextField('Notes')
    submit = SubmitField('   Create   ')

    def validate_title(self, title):
        shopping_list = ShoppingList.query.filter_by(title=title.data).first()
        if shopping_list is not None:
            raise ValidationError('This title already exists.')


# class ShoppingListItemForm(FlaskForm):