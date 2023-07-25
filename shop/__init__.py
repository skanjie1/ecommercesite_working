from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, configure_uploads, UploadSet
from flask_msearch import Search
from flask_login import LoginManager
import os

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__) 
db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config['SECRET_KEY'] = 'jwkhfciuewhfwzf323f3'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

photos = UploadSet("photos", IMAGES)
configure_uploads(app, photos)
# patch_request_class(app)

db.init_app(app)
bcrypt = Bcrypt(app)
search = Search()
search.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='customerLogin'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message = u"Please login"

from shop.admin import routes
from shop.products import routes
from shop.carts import carts
from shop.customers import routes
