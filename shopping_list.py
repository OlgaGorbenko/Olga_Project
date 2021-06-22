# noinspection PyUnresolvedReferences
import food_app.models
# noinspection PyUnresolvedReferences
import food_app.routes
from food_app.app_factory import app, db
from food_app.models import Product

# from food_app.actions import add_user


# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'User': User, 'Post': Post}


# add_user()

if __name__ == '__main__':
    app.run()

