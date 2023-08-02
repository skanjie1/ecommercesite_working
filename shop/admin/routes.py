from flask import render_template, session, request, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user, login_user
from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User
from shop.customers.model import CustomerOrder, Review
from shop.products.models import Addproduct, Brand, Category
import os

@app.route('/')
def home():
    # return "Welcome to my shop"
    return render_template('layout.html', title='Home page')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact Us')

@app.route('/about')
def about():
    return render_template('about.html', title='About Us')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/dashboard')
# @login_required
def dashboard():
    total_items = Addproduct.query.count()
    total_brands = Brand.query.count()
    total_categories = Category.query.count()
    total_orders = CustomerOrder.query.count()
    total_reviews = Review.query.count()

    products = Addproduct.query.all()
    return render_template('admin/admin.html', title='Dashboard', products=products, total_items=total_items, total_brands=total_brands, total_categories=total_categories, total_orders=total_orders, total_reviews=total_reviews)

@app.route('/reviews')
def admin_reviews():
    reviews = Review.query.order_by(Review.pub_date.desc()).all()
    return render_template('admin/reviews.html', reviews=reviews)

@app.route('/adminpage')
def adminpage():  
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    products = Addproduct.query.all()
    return render_template('admin/index.html', title='Admin Page', products=products)

@app.route('/brands')
def brands():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    total_brands = Brand.query.count()
    return render_template('admin/brand.html', title="Brand page", brands=brands, total_brands=total_brands)

@app.route('/category')
def category():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    total_categories = Category.query.count()
    return render_template('admin/brand.html', title="Brand page", categories=categories, total_categories=total_categories)

 
# -------------------------
# @app.route('/admin')
# def admin():
#     if 'email' not in session:
#         flash(f'PLease login first', 'danger')
#         return redirect(url_for('login'))
#     products = Addproduct.query.all()
#     return render_template('admin/index.html', title='Admin Page', products=products)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        db.session.commit() 
        flash(f'Welcome {form.name.data}. Thank you for registering', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('admin/register.html', form=form, title="Registration page")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome {form.email.data}. You are logged in', 'success')
            return redirect(request.args.get('next') or url_for('dashboard'))
        else:
            flash('Wrong Password, please try again', 'danger')
            return redirect(url_for('login'))
        
    return render_template('admin/login.html', form=form, title="Login Page")

# @app.route('/logout')
# def admin_logout():
#     logout_user()
#     return redirect(url_for('login'))

