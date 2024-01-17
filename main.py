from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Mock product data for different domains
products = {'orientindia.net': 'Orient India Products', 'amazon.in': 'Amazon India Products'}

# Initialize an empty cart for each user
carts = {}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form.get('user_email', '')
        domain = user_email.split('@')[-1]

        if domain in products:
            # Initialize an empty cart for the user
            carts[user_email] = []
            return redirect(url_for('index', user_email=user_email))
        else:
            return render_template('login.html', error='Access Denied: Unauthorized domain please Connect to Customer Care')

    return render_template('login.html', error=None)

@app.route('/index')
def index():
    user_email = request.args.get('user_email', '')
    domain = user_email.split('@')[-1]

    if domain in products:
        user_products = products[domain]
        if domain == 'orientindia.net':
            return render_template('orient.html', user_products=user_products, user_email=user_email)
        elif domain == 'amazon.in':
            return render_template('amazon.html', user_products=user_products, user_email=user_email)
    else:
        return "Access Denied: Unauthorized domain"


@app.route('/cart')
def cart():
    user_email = request.args.get('user_email', '')

    # Get the user's cart
    user_cart = carts.get(user_email, [])

    return render_template('cart.html', user_cart=user_cart, user_email=user_email)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    user_email = request.form.get('user_email', '')
    product_details = {
        'name': request.form.get('product_name', ''),
        'image': request.form.get('product_image', ''),
        'description': request.form.get('product_description', ''),
        'rating': request.form.get('product_rating', ''),
        'price': request.form.get('product_price', ''),
    }


    # Add the product details to the user's cart
    carts.setdefault(user_email, []).append(product_details)

    return redirect(url_for('index', user_email=user_email))

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    user_email = request.form.get('user_email', '')
    product_name = request.form.get('product_name', '')

    # Remove the product from the user's cart
    if user_email in carts:
        updated_cart = [product for product in carts[user_email] if product['name'] != product_name]
        carts[user_email] = updated_cart

    # Redirect back to the cart page
    return redirect(url_for('cart', user_email=user_email))



if __name__ == '__main__':
    app.run(debug=True)
