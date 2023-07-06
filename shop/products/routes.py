from flask import redirect, render_template, url_for,flash, request, session
from shop import db, app, photos
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import secrets

# @app.route('/')
# def home():
#     return ""

@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'PLease login first', 'danger')
        return redirect(url_for('login'))
    products = Addproduct.query.all()
    return render_template('admin/index.html', title='Admin Page', products=products)

@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'Brand {getbrand} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addcategory'))
    
    return render_template('products/addbrand.html', brands='brands') 

# @app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
# def updatebrand(id):
#     if 'email' not in session:
#         flash(f,'Please log in first','danger')
#     updatebrand = Brand.query.get_or_404(id)
#     brand = request.form.get('brand')
#     if request.method == "POST":
#         updatebrand.name = brand
#         flash(f'Brand successfully updated','success')
#         db.session.commit()
#         return redirect(url_for('brands'))
#     return render_template('products/updatebrand.html', title='Update Brand Page', updatebrand=updatebrand)

@app.route('/addcategory', methods=['GET', 'POST'])
def addcategory():
    if request.method == "POST":
        getcategory = request.form.get('category')
        category = Category(name=getcategory)
        db.session.add(category)
        flash(f'Category {getcategory} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addcategory'))
    
    return render_template('products/addbrand.html') 

# @app.route('/updatecategory/<int:id>', methods=['GET', 'POST'])
# def updatecategory(id):
#     if 'email' not in session:
#         flash(f,'Please log in first','danger')
#     updatecategory = Category.query.get_or_404(id)
#     category = request.form.get('category')
#     if request.method == "POST":
#         updatecategory.name = category
#         flash(f'Category successfully updated','success')
#         db.session.commit()
#         return redirect(url_for('category'))
#     return render_template('products/updatebrand.html', title='Update Category Page', updatecategory=updatecategory)

@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.desc.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        
        # image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_1 = photos.save(request.files.get('image_1'))
        image_2 = photos.save(request.files.get('image_2'))
        image_3 = photos.save(request.files.get('image_3'))

        addproduct = Addproduct(name=name, price=price, discount=discount, stock=stock, colors=colors, desc=desc, brand_id=brand, category_id=category, image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(addproduct)
        flash(f'Product {name} has been added to your database','success')
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('products/addproduct.html', title="Add Product page", form=form, brands=brands, categories=categories)

