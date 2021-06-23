# from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .app_factory import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
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
    title = db.Column(db.String(256), index=True, unique=True)
    type_of_product = db.Column(db.String(120), index=True)
    unit_of_measure = db.Column(db.String(120), index=True)

    def __repr__(self):
        return '<Product {}>'.format(self.title)


# class ShoppingList(db.Model):
#     title = db.Column(db.String(256), index=True, unique=True, primary_key=True)  # pkey?
#     owner = db.Column(db.String, db.ForeignKey('user.id'))
#     items = db.relationship('ShoppingListItem') #backref='author', lazy='dynamic'
#
#     def __repr__(self):
#         return '<Product {}>'.format(self.title)

# class ShoppingListItem(db.Model):
#     shopping_list = db.Column(db.String, db.ForeignKey('shopping_list.title'))  #?? # pkey?
#     product = db.Column(db.String, db.ForeignKey('product.id'))
#     quantity = db.Column(db.Integer, index=True)
#     is_buyed = db.Column(db.Bool, index=True)
#
#     def __repr__(self):
#         return '<Product {}>'.format(self.shopping_list)  #?
#
# class Recipe(db.Model):
#     title = db.Column(db.String(256), index=True, unique=True, primary_key=True)  # pkey?
#     ingredients = db.relationship('Ingredient') #backref='author', lazy='dynamic'
#
#     def __repr__(self):
#         return '<Product {}>'.format(self.title)
#
# class Ingredient(db.Model):
#     recipe = db.Column(db.String, db.ForeignKey('recipe.title'))  # pkey?
#     product = db.Column(db.String, db.ForeignKey('product.id'))
#     quantity = db.Column(db.Integer, index=True)
#     unit_of_measure = db.Column(db.String(120), index=True)
#
#     def __repr__(self):
#         return '<Product {}>'.format(self.recipe)  #?




# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
#     def __repr__(self):
#         return '<Post {}>'.format(self.body)
