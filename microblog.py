# noinspection PyUnresolvedReferences
import blog_app.models
# noinspection PyUnresolvedReferences
import blog_app.routes
from blog_app.app_factory import app, db
from blog_app.models import User, Post

from blog_app.actions import delete_all_users


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}


delete_all_users()

if __name__ == '__main__':
    app.run()