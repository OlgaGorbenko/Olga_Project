# noinspection PyUnresolvedReferences
import food_app.models
# noinspection PyUnresolvedReferences
import food_app.routes
from food_app.app_factory import app, db
from food_app.models import Product

from food_app.actions import add_product


# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'User': User, 'Post': Post}


add_product()

if __name__ == '__main__':
    app.run()