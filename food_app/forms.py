from flask_admin.contrib.sqla.fields import QuerySelectField
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, SelectField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from food_app.constants import units_of_measure
from food_app.models import User, Product, Recipe, ShoppingList, ShoppingListItem


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


class AddProductForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    type_of_product = SelectField('Type of Product', choices=[
        ('other', 'other'),
        ('fruit', 'fruit'),
        ('vegetable', 'vegetable'),
        ('meat', 'meat'),
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
    # ingredients = StringField('Ingredients')
    description = TextField('Description')
    submit = SubmitField('   Add   ')

    def validate_title(self, title):
        recipe = Recipe.query.filter_by(title=title.data).first()
        if recipe is not None:
            raise ValidationError('This title already exists.')


class AskDeleteRecipeForm(FlaskForm):
    ask = SelectField('Delete?', choices=[
        ('yes', 'yes'),
        ('no', 'no'),
        # (True, 'yes'),
        # (False, 'no'),
    ])
    submit = SubmitField('Submit')


class NewShoppingListForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    notes = TextField('Notes')
    submit = SubmitField('   Create   ')

    def validate_title(self, title):
        shopping_list = ShoppingList.query.filter_by(title=title.data).first()
        if shopping_list is not None:
            raise ValidationError('This title already exists.')


class AskDeleteShoppingListForm(FlaskForm):
    ask = SelectField('Delete?', choices=[
        ('yes', 'yes'),
        ('no', 'no'),
        # (True, 'yes'),
        # (False, 'no'),
    ])
    submit = SubmitField('Submit')


def all_lists_titles():
    owner = current_user.id
    return ShoppingList.query.filter_by(owner=owner)


class AddPortionsForm(FlaskForm):
    title_list = QuerySelectField('Select a Shopping List', query_factory=all_lists_titles, allow_blank=False)
    number_of_portions = SelectField('Number of Portions', choices=[
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ])
    submit = SubmitField('   Add Portions   ')


def all_products_titles():
    return Product.query.order_by(Product.title)


class AddProductToListForm(FlaskForm):
    shopping_list = QuerySelectField('Select a Shopping List', query_factory=all_lists_titles, allow_blank=False)
    # product_to_add = QuerySelectField('Product', query_factory=all_products_titles, allow_blank=False)
    quantity = IntegerField('Quantity', default=1)
    # unit_of_measure = SelectField('Unit of Measure', choices=units_of_measure)
    submit = SubmitField('      Add to Shopping List      ')


def all_recipes_titles():
    owner = current_user.id
    return Recipe.query.filter_by(owner=owner)


class AddProductToRecipeForm(FlaskForm):
    recipe = QuerySelectField('Select a Recipe', query_factory=all_recipes_titles, allow_blank=False)
    # product_to_add = QuerySelectField('Product', query_factory=all_products_titles, allow_blank=False)
    quantity = IntegerField('Quantity', default=1)
    # unit_of_measure = SelectField('Unit of Measure', choices=units_of_measure)
    submit = SubmitField('           Add to Recipe           ')


class ChangeQuantityItemForm(FlaskForm):
    # item = ShoppingListItem.query.filter_by(id=item.id).first()
    quantity = IntegerField('Quantity', default=0)
    submit = SubmitField('                 Submit                 ')


class ChangeQuantityIngredientForm(FlaskForm):
    # item = ShoppingListItem.query.filter_by(id=item.id).first()
    quantity = IntegerField('Quantity', default=0)
    submit = SubmitField('                 Submit                 ')


class EditDescriptionForm(FlaskForm):
    description = TextField('New description:')
    submit = SubmitField('                 Submit                 ')


class AddNotesToListForm(FlaskForm):
    notes = TextField('Add Notes:')
    submit = SubmitField('                 Submit                 ')


class SelectProductToAddForm(FlaskForm):
    select_product_to_add = QuerySelectField('Product', query_factory=all_products_titles, allow_blank=False)
    submit = SubmitField('  Select Product  ')

