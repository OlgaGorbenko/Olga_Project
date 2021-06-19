# from datetime import datetime

from .app_factory import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(256), index=True, unique=True)
    type_of_product = db.Column(db.String(120), index=True)
    units = db.Column(db.String(120), index=True)

    def __repr__(self):
        return '<Product {}>'.format(self.product_name)


# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
#     def __repr__(self):
#         return '<Post {}>'.format(self.body)
