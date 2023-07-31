from flask import redirect, render_template, url_for,flash, request, session, current_app, make_response
from flask_login import login_required, current_user, logout_user, login_user
from shop import db, app, photos, search, bcrypt, login_manager
from .forms import CustomerRegisterForm, CustomerLoginForm
from .model import Register, CustomerOrder
from shop.products.models import Addproduct
import secrets, os
import stripe
import pdfkit

publishable_key ='pk_test_51NYNtSFRhtvUWoeCZPlXkOK2By9c4flbaTz5pXuBTQ5F7FMclyzTNqzmY9Z9yLWf9HD4ARnGZEbDFn9WWXFuR2A200og3ph3xW'
stripe.api_key = 'sk_test_51NYNtSFRhtvUWoeCU8mUOTG9jzNNraUXLGK2RZ3sMt7kLowrMykIOqzfg35ahNeDj1bkm0UC44EyeEpeKjyow3i400iJCWO5ME'

@app.route('/payment', methods=['POST'])
@login_required
def payment():
    invoice = request.form.get('invoice')
    amount= request.form.get('amount')
    
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
    )
    
    charge = stripe.Charge.create(
        customer=customer.id,
        description='MochiMochi',
        amount=amount,
        currency='usd',        
    )
    orders = CustomerOrder.query.filter_by(customer_id=current_user.id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
    orders.status='Paid'
    db.session.commit()
    return redirect(url_for('thanks'))

@app.route('/thanks')
def thanks():
    orders = CustomerOrder.query.filter_by(customer_id=current_user.id).order_by(CustomerOrder.id.desc()).first()

    return render_template('customer/thanks.html', orders=orders)

@app.route('/explore')
def explore():
    return render_template('customer/explore.html')

@app.route('/customer/register', methods=['GET','POST'])
def customer_register():
    form = CustomerRegisterForm() 
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        is_admin = False 
        if form.username.data == 'admin':
            is_admin = True
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password, country=form.country.data, city=form.city.data, address=form.address.data, zipcode=form.zipcode.data)
        db.session.add(register)
        db.session.commit()
        flash(f'Welcome {form.name.data}, Thank you for registering','success')
        return redirect(url_for('customerLogin'))
    
    return render_template('customer/register.html', form=form)


@app.route('/customer/login', methods=['GET', 'POST'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        # user = Register.query.all()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            # session['email'] = form.email.data
            flash(f'Welcome {form.email.data}, You are logged in!','success')
            next = request.args.get('next')
            return redirect(next or url_for('products'))
        else:
            flash('Incorrect email and password','danger')
            return redirect(url_for('customerLogin'))
    
    return render_template('/customer/login.html', form=form)

@app.route('/customer/logout')
def customer_logout():
    logout_user()
    
    return redirect(url_for('customerLogin'))

def updateshoppingcart():
    for _key, product in session['Shoppingcart'].items():
        session.modified = True
        del product['image']
        del product['colors']
    return updateshoppingcart


@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        updateshoppingcart()
        try:
            order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Your order has been sent successfully','success')
            return redirect(url_for('orders', invoice=invoice))
        except Exception as e:
            print(e)
            flash('Something went wrong while getting order','danger')
            return redirect(url_for('getCart'))
        
@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        # total = 0 
        grandtotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id, invoice=invoice).order_by(CustomerOrder.id.desc()).first()
        for _key, product in orders.orders.items():
            # discount = (product['discount']) *float(product['price'])
            # subtotal += float(product['price']) * int(product['quantity'])
            # subtotal -= discount
            price = float(product['price'])
            quantity = int(product['quantity'])
            discount = (product['discount'])
            total = (price - discount) * quantity
            grandtotal += total

            grandtotal = round(grandtotal, 2)
 
    
    else:
        return redirect(url_for('customerLogin'))
    return render_template('customer/order.html', invoice=invoice, grandtotal=grandtotal, customer=customer, orders=orders)

# @app.route('/admin/orders')
# @login_required
# def admin_orders():
#     if current_user.is_authenticated and current_user.is_admin:
#         orders = CustomerOrder.query.all()
#         for order in orders:
#             total = 0
#             for _, product in order.orders.items():
#                 price = float(product['price'])
#                 quantity = int(product['quantity'])
#                 discount = float(product['discount'])
#                 total += (price - discount) * quantity
#             total = round(total, 2)
#             order.total = total 

#     else:
#         return redirect(url_for('login'))

#     return render_template('admin/orders.html', orders=orders)



@app.route('/admin/orders')
def admin_orders():
    # orders = CustomerOrder.query.all()
    orders = CustomerOrder.query.order_by(CustomerOrder.date_created.desc()).all()

    return render_template('admin/orders.html', orders=orders)

@app.route('/delete_order/<int:order_id>', methods=['POST', 'DELETE'])
# @login_required
def delete_order(order_id):
    if request.method == 'POST':
        order = CustomerOrder.query.get_or_404(order_id)
        db.session.delete(order)
        db.session.commit()

        flash('Order has been deleted successfully.', 'success')
    return redirect(url_for('admin_orders'))


@app.route('/getpdf/<invoice>',methods=['POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        # total = 0 
        grandtotal = 0
        customer_id = current_user.id
        if request.method == "POST":
            customer = Register.query.filter_by(id=customer_id).first()
            orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
            for _key, product in orders.orders.items():
                price = float(product['price'])
                quantity = int(product['quantity'])
                discount = (product['discount'])
                total = (price - discount) * quantity
                grandtotal += total

                grandtotal = round(grandtotal, 2)
 
            # config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
  
            rendered= render_template('customer/pdf.html', invoice=invoice, grandtotal=grandtotal, customer=customer, orders=orders)
            pdf = pdfkit.from_string(rendered, False)
            response = make_response(pdf)
            response.headers['content-Type']='application/pdf'
            response.headers['content-Disposition'] = 'inline: filename='+invoice+'.pdf'
            return response
    return request(url_for('home'))

  

  
 

