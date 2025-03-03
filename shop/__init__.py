from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, configure_uploads, UploadSet
from flask_msearch import Search
from flask_login import LoginManager
from flask_migrate import Migrate
from textblob import TextBlob
from shop.admin.admin_resources import AdminRegistrationResource, AdminLoginResource

# from shop.utils import has_purchased_product
# from shop import db
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

jwt = JWTManager(app)
api = Api(app)


api.add_resource(AdminRegistrationResource, '/api/admin/register')
api.add_resource(AdminLoginResource, '/api/admin/login')


migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='customerLogin'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message_category ='danger'
login_manager.login_message = "Hello! Please login first"

from shop.customers.model import CustomerOrder

def has_purchased_product(user_id, product_id):
    order = CustomerOrder.query.filter_by(customer_id=user_id).first()
    if order:
        orders = order.orders
        if str(product_id) in orders:
            return True
    return False

app.jinja_env.globals['has_purchased_product'] = has_purchased_product


from shop.admin import routes
from shop.products import routes
from shop.carts import carts
from shop.customers import routes

