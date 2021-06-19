from flask_admin.contrib.sqla import ModelView
from food_app.models import Product

from .app_factory import admin, db

# admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(Product, db.session))
