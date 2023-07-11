from flask import redirect, render_template, url_for,flash, request, session, current_app
from shop import db, app, photos
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import secrets, os

# @app.route('/home')
# def home():
#     return render_template('layout.html')

@app.route('/products')
def products():
    products = Addproduct.query.filter(Addproduct.stock > 0)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return render_template('products/index.html', products=products, brands=brands)

@app.route('/brand/<int:id>')
def get_brand(id):
    brand = Addproduct.query.filter_by(brand_id=id)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()

    return render_template('products/index.html', brand=brand, brands=brands)

@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'Brand {getbrand} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    
    return render_template('products/addbrand.html', brands='brands') 


@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == "POST":
        updatebrand.name = brand
        flash(f'Brand successfully updated','success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', title='Update Brand Page', updatebrand=updatebrand)

@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(brand)
        db.session.commit()
        flash(f'Brand {brand.name} successfully deleted','success')
        return redirect(url_for('brands'))
    flash(f'Brand {brand.name} cant be deleted','danger')
    return redirect(url_for('brands'))
        
@app.route('/addcategory', methods=['GET', 'POST'])
def addcategory():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getcategory = request.form.get('category')
        category = Category(name=getcategory)
        db.session.add(category)
        flash(f'Category {getcategory} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addcategory'))
    
    return render_template('products/addbrand.html') 

@app.route('/updatecategory/<int:id>', methods=['GET', 'POST'])
def updatecategory(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == "POST":
        updatecategory.name = category
        flash(f'Category successfully updated','success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatebrand.html', title='Update Category Page', updatecategory=updatecategory)

@app.route('/deletecategory/<int:id>', methods=['POST'])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(category)
        db.session.commit()
        flash(f'Category {category.name} successfully deleted','success')
        return redirect(url_for('category'))
    flash(f'Category {category.name} cant be deleted','danger')
    return redirect(url_for('category'))

@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
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
        return redirect(url_for('adminpage'))

    return render_template('products/addproduct.html', title="Add Product page", form=form, brands=brands, categories=categories)

@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    form = Addproducts(request.form)
    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.brand_id = brand
        product.category_id = category
        product.colors = form.colors.data
        product.desc = form.desc.data
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'))
            except:
                product.image_1 = photos.save(request.files.get('image_1'))
                
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                product.image_1 = photos.save(request.files.get('image_2'))
            except:
                product.image_1 = photos.save(request.files.get('image_2'))
                
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                product.image_1 = photos.save(request.files.get('image_3'))
            except:
                product.image_1 = photos.save(request.files.get('image_3'))

        db.session.commit()
        flash(f'Product updated successfully','success')
        return redirect(url_for('adminpage'))
        
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.desc.data = product.desc
    return render_template('products/updateproduct.html', form=form, brands=brands, categories=categories, product=product)

@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    
    product = Addproduct.query.get_or_404(id)
    
    if request.method == "POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        except Exception as e:
            print(e)
        
        db.session.delete(product)
        db.session.commit()
        flash(f'Product {product.name} successfully deleted','success')
        return redirect(url_for('adminpage'))
    
    flash(f'Product {product.name} cant be deleted','danger')
    
    return redirect(url_for('adminpage'))
        