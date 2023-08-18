from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, configure_uploads, UploadSet
from flask_msearch import Search
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)
db = SQLAlchemy()
bcrypt = Bcrypt(app)
search = Search()
jwt = JWTManager(app)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config['SECRET_KEY'] = 'jwkhfciuewhfwzf323f3'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/images')

photos = UploadSet("photos", IMAGES)
configure_uploads(app, photos)

db.init_app(app)
search.init_app(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'customerLogin'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message_category = 'danger'
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

from shop.admin.admin_resources import AdminRegistrationResource, AdminLoginResource
api.add_resource(AdminRegistrationResource, '/api/admin/register')
api.add_resource(AdminLoginResource, '/api/admin/login')



with app.app_context():
    db.create_all()

