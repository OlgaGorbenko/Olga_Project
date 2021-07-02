from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .app_factory import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    # posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True, unique=True, nullable=False)
    type_of_product = db.Column(db.String(120))
    unit_of_measure = db.Column(db.String(120))

    def __repr__(self):
        return '<Product {}>'.format(self.title)

    def __str__(self):
        return f'{self.title}'.capitalize()  # Big first letter only.


class ShoppingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), default='')
    owner = db.Column(db.ForeignKey('user.id'))
    items = db.relationship('ShoppingListItem', backref='shopping_list', lazy='dynamic')
    notes = db.Column(db.Text)

    def __repr__(self):
        return '<ShoppingList {}>'.format(self.title)


class ShoppingListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shopping_list_id = db.Column(db.ForeignKey('shopping_list.id'))
    product_id = db.Column(db.ForeignKey('product.id'))
    product = db.relationship('Product')
    # ingredient_id = db.Column(db.ForeignKey('ingredient.id'))
    # ingredient = db.relationship('Ingredient')
    quantity = db.Column(db.Integer)
    unit_of_measure = db.Column(db.String(120))
    is_buyed = db.Column(db.Boolean)

    def __repr__(self):
        return f'<ShoppingListItem {self.product.title}>'


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True, unique=True, nullable=False)
    ingredients = db.relationship('Ingredient', backref='recipe', lazy='dynamic')
    description = db.Column(db.Text)

    def __repr__(self):
        return '<Recipe {}>'.format(self.title)

    def __str__(self):
        return f'{self.title}'.title()  # All first letters are big.


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.ForeignKey('recipe.id'))
    product_id = db.Column(db.ForeignKey('product.id'))
    product = db.relationship('Product')
    quantity = db.Column(db.Integer)
    unit_of_measure = db.Column(db.String(120))

    def __repr__(self):
        return '<Ingredient {}>'.format(self.product)

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
#     def __repr__(self):
#         return '<Post {}>'.format(self.body)
