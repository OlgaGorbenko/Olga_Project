from flask import url_for, request
from flask_admin.contrib import sqla
from werkzeug.utils import redirect

from food_app.models import Product
from .app_factory import admin, db, login


class MicroBlogModelView(sqla.ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


admin.add_view(MicroBlogModelView(Product, db.session))
