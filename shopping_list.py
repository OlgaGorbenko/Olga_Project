# noinspection PyUnresolvedReferences
# noinspection PyUnresolvedReferences
import food_app.admin
import food_app.models
# noinspection PyUnresolvedReferences
import food_app.routes
from food_app.app_factory import app

# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'User': User, 'Post': Post}


if __name__ == '__main__':
    app.run()
