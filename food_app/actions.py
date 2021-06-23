from food_app.app_factory import app, db
from food_app.models import User, Product


# def add_user():
#     user = User(username='lin', email='lin@example.com')
#     user.set_password('cat')
#     db.session.add(user)
#     db.session.commit()
#     return user


def add_product():
    product = Product(product_name='salmon', type_of_product='fish', units='grams')
    db.session.add(product)
    db.session.commit()
    return product


def return_all_products():
    products = Product.query.all()
    for product in products:
        print(product.id, product.title, product.type_of_product)


def return_product():
    product = Product.query.get(1)
    print(product)


def delete_all_products():
    products = Product.query.all()
    for product in products:
        db.session.delete(product)
    db.session.commit()


# def add_post():
#     user = Product.query.get(2)
#     post = Post(body='new post!', author=user)
#     db.session.add(post)
#     db.session.commit()
#
#
# def return_posts_only():
#     posts = Post.query.all()
#     print(posts)
#
#
# def return_all_posts():
#     posts = Post.query.all()
#     for post in posts:
#         print(post.id, post.author.product_name, post.body)
#
#
# def delete_all_posts():
#     posts = Post.query.all()
#     for post in posts:
#         db.session.delete(post)
#     db.session.commit()

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database