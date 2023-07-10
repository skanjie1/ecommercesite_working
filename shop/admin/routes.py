from flask import render_template, session, request, redirect, url_for, flash

from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User
from shop.products.models import Addproduct, Brand, Category
# from shop.products.models import Addproduct, Brand, Category
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
    return render_template('admin/brand.html', title="Brand page", brands=brands)

@app.route('/category')
def category():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html', title="Brand page", categories=categories)

 
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
        return redirect(url_for('adminpage'))
    
    return render_template('admin/register.html', form=form, title="Registration page")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome {form.email.data}. You are logged in', 'success')
            return redirect(request.args.get('next') or url_for('adminpage'))
        else:
            flash('Wrong Password, please try again', 'danger')
            return redirect(url_for('login'))
        
    return render_template('admin/login.html', form=form, title="Login Page")