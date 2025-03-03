from flask import redirect, render_template, url_for,flash, request, session, current_app
from shop import db, app
from shop.products.models import Addproduct


def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        colors = request.form.get('colors')
        product = Addproduct.query.filter_by(id=product_id).first()
        
        if product_id and quantity and colors and request.method == "POST":
            DictItems = {product_id:{'name': product.name, 'price':float(product.price), 'discount':product.discount, 'color':colors, 'quantity': quantity, 'image':product.image_1, 'colors':product.colors}}
            
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    # for key, item in session['Shoppingcart'].items():
                    #     if int(key) == int(product_id):
                    #         for product in session['Shoppingcart'].values():
                    #             session.modified = True
                    #             iquantity = print(product['quantity'])
                    #             flash(product_id,'success')
                    #             flash(iquantity,'success')
                    #             iquantity+=1
                    #             item['quantity'] = iquantity
                    #             flash('Product updated successfully','success')
                    #             return redirect(url_for('getCart'))
                    for key, item in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            quantity = item.get('quantity', 0)
                            item['quantity'] = item['quantity'] + 1
                    # print("Product already in cart")
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'], DictItems)
                    flash('Product added to cart','success')
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
                
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)
    
@app.route('/carts')
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('products'))
    
    grandtotal = 0

    for product in session['Shoppingcart'].values():
        price = float(product['price'])
        quantity = int(product['quantity'])
        discount = (product['discount'])
        total = (price - discount) * quantity
        grandtotal += total

    grandtotal = round(grandtotal, 2)
    
    return render_template('products/carts.html', grandtotal=grandtotal)


@app.route('/updatecart/<int:id>', methods=['GET', 'POST'])
def updatecart(id):
    if 'Shoppingcart' not in session and len(session.get('Shoppingcart', {})) <= 0:
        return redirect(url_for('products'))

    cart = session['Shoppingcart']
    product = cart.get(str(id))  
    if not product:
        flash('Product not found in cart', 'danger')
        return redirect(url_for('getCart'))

    if request.method == "POST":
        quantity = request.form.get('quantity')
        color = request.form.get('colors')

        try:
            session.modified = True
            for key, item in cart.items():
                if int(key) == id:
                    item['quantity'] = quantity
                    item['color'] = color  
                    flash('Product updated successfully!', 'success')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            flash('Error updating product', 'danger')
            return redirect(url_for('getCart'))

    return render_template('products/updatecart.html', product=product)


@app.route('/cartupdate/<int:id>', methods=['GET', 'POST'])
def cartupdate(id):
    if 'Shoppingcart' not in session and len(session.get('Shoppingcart', {})) <= 0:
        return redirect(url_for('products'))

    product = Addproduct.query.filter_by(id=id).first()
    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('getCart'))

    return render_template('products/updatecart.html', product=product)


@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session and len(session('Shoppingcart')) <= 0:
        return redirect(url_for('products'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                flash('Product removed successfully!','success')
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))

@app.route('/clearcart')
def clearcart():
    try:
        session.pop('Shoppingcart', None)
        flash('Cart cleared succesfully!','success')
        return redirect(url_for('products'))
    except Exception as e:
        print(e)
        
@app.route('/cartresult')
def cartresult():
    searchword = request.args.get('q')
    search_results = []

    if 'Shoppingcart' in session:
        for key, product in session['Shoppingcart'].items():
            product_name = product['name'].lower()
            if searchword.lower() in product_name:
                product['id'] = key
                search_results.append(product)

    if len(search_results) == 0:
        flash('Item not found', 'danger')
    return render_template('products/cartresult.html', products=search_results)