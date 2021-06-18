from blog_app.app_factory import app, db
from blog_app.models import User, Post


def add_user():
    user = User(username='lin', email='lin@example.com')
    db.session.add(user)
    db.session.commit()
    return user


def delete_all_users():
    users = User.query.all()
    for user in users:
        db.session.delete(user)
    db.session.commit()


def return_all_users():
    users = User.query.all()
    for user in users:
        print(user.id, user.username)


def return_user():
    user = User.query.get(1)
    print(user)


def add_post():
    user = User.query.get(2)
    post = Post(body='new post!', author=user)
    db.session.add(post)
    db.session.commit()


def return_posts_only():
    posts = Post.query.all()
    print(posts)


def return_all_posts():
    posts = Post.query.all()
    for post in posts:
        print(post.id, post.author.username, post.body)


def delete_all_posts():
    posts = Post.query.all()
    for post in posts:
        db.session.delete(post)
    db.session.commit()

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database