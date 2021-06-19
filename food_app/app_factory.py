from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
admin = Admin(app, name='microblog', template_mode='bootstrap3')

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)