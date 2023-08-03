from shop.customers.model import CustomerOrder

def has_purchased_product(user_id, product_id):
    order = CustomerOrder.query.filter_by(customer_id=user_id).first()
    if order:
        orders = order.orders
        if str(product_id) in orders:
            return True
    return False
