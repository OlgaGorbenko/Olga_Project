from flask import url_for, request
from flask_admin.contrib.sqla import ModelView
from flask_admin.model.form import InlineFormAdmin
from flask_login import current_user
from werkzeug.utils import redirect

from food_app.models import User, Product, Recipe, Ingredient, ShoppingList
from .app_factory import admin, db


class MicroBlogModelView(ModelView):
    # can_delete = False  # disable model deletion
    # page_size = 50  # the number of entries to display on the list view
    # can_create = False
    # can_edit = False
    can_view_details = True
    # column_exclude_list = ['password', ]
    # column_searchable_list = ['name', 'email']
    # column_filters = ['country']
    # column_editable_list = ['name', 'last_name']
    # create_modal = True
    # edit_modal = True
    # form_excluded_columns = ['last_name', 'email']
    form_widget_args = {
        'description': {
            'rows': 10,
            'style': 'color: black'
        }
    }
    can_export = True
    form_choices = {
        'unit_of_measure': [
            ('gram', 'g'),
            ('milliliter', 'mL'),
            ('piece', 'pc')
        ],
        'type_of_product': [
            ('fruit', 'fruit'),
            ('vegetable', 'vegetable'),
            ('meet', 'meet'),
            ('fish', 'fish'),
            ('milk', 'milk'),
            ('grain', 'grain'),
            ('sweets', 'sweets'),
            ('spice and souse', 'spice and souse'),
            ('beverage', 'beverage'),
            ('other', 'other')
        ]
    }

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class RecipeAdminView(MicroBlogModelView):
    # inline_models = ((Ingredient, dict(form_columns=['title'])), )
    inline_models = (Ingredient,)


class IngredientInlineModelForm(InlineFormAdmin):
    # form_columns = ('title', 'date')
    form_choices = {
        'unit_of_measure': [
            ('gram', 'g'),
            ('milliliter', 'mL'),
            ('piece', 'pc')
        ]
    }


class MyMicroBlogModelView(MicroBlogModelView):
    inline_models = (IngredientInlineModelForm(Ingredient),)


admin.add_view(MicroBlogModelView(User, db.session))
admin.add_view(MicroBlogModelView(Product, db.session))
admin.add_view(RecipeAdminView(Recipe, db.session))
admin.add_view(MicroBlogModelView(ShoppingList, db.session))
