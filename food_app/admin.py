from flask import url_for, request
from flask_admin.contrib import sqla
from werkzeug.utils import redirect
from flask_admin.contrib.sqla import ModelView

from .app_factory import admin, db, login
from food_app.models import User


# class MicroBlogModelView(ModelView):
#     can_delete = False  # disable model deletion
#     page_size = 50  # the number of entries to display on the list view


class MicroBlogModelView(sqla.ModelView):
    can_delete = False  # disable model deletion
    page_size = 50  # the number of entries to display on the list view
    can_create = False
    can_edit = False
    can_view_details = True
    column_exclude_list = ['password', ]
    column_searchable_list = ['name', 'email']
    column_filters = ['country']
    column_editable_list = ['name', 'last_name']
    create_modal = True
    edit_modal = True
    form_excluded_columns = ['last_name', 'email']
    form_widget_args = {
        'description': {
            'rows': 10,
            'style': 'color: black'
        }
    }
    can_export = True


    def is_accessible(self):
        return login.current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


admin.add_view(MicroBlogModelView(User, db.session))
# admin.add_view(MicroBlogModelView(Post, db.session))
