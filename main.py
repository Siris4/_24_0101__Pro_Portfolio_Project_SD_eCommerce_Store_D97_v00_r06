# main.py
from flask import Flask, render_template, request, jsonify
import stripe
from stripe_config import stripe

app = Flask(__name__)

# Dummy data for products
PRODUCTS = [
    {'id': 'product1', 'name': 'Physical Product 1', 'price': 100, 'description': 'A cool item', 'image': 'item1.jpg'},
    {'id': 'product2', 'name': 'Physical Product 2', 'price': 7500, 'description': 'Another cool item',
     'image': 'item2.jpg'},
    {'id': 'service1', 'name': 'Web Design Service', 'price': 68000,
     'description': 'Custom web design for your needs.'},
    {'id': 'service2', 'name': 'Home Automation Service', 'price': 30000, 'description': 'Complete smart home setup.'}
]


@app.route('/')
def home():
    return render_template('home.html', products=PRODUCTS)


@app.route('/product/<product_id>')
def product_page(product_id):
    product = next((item for item in PRODUCTS if item['id'] == product_id), None)
    if product:
        return render_template('product.html', product=product)
    else:
        return "Product not found", 404


@app.route('/checkout', methods=['POST'])
def checkout():
    product_id = request.form.get('product_id')
    product = next((item for item in PRODUCTS if item['id'] == product_id), None)

    if product:
        try:
            # Create a new PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=product['price'],
                currency='usd',
                payment_method_types=['card'],
                metadata={'product_id': product['id']}
            )
            return render_template('checkout.html', client_secret=intent.client_secret, product=product)
        except Exception as e:
            return jsonify(error=str(e)), 403
    return "Product not found", 404


if __name__ == '__main__':
    app.run(debug=True)
