from flask import Flask, render_template, request, redirect, url_for
from jinja2 import Environment
app = Flask(__name__)

# Mock product data for different domains
products = {'orientindia.net': 'Orient India Products', 'amazon.in': 'Amazon India Products',
            'apple.in': 'Apple India Products', 'apple.com': 'Apple Products'}
app.jinja_env.globals.update({'float': float})  # Make float available in templates
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
            return render_template('login.html', error='Access Denied: Unauthorized domain please connect to customer care')

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
        elif domain == 'apple.in':
            return render_template('apple.html', user_products=user_products, user_email=user_email)
        elif domain == 'apple.com':
            return render_template('apple.html', user_products=user_products, user_email=user_email)

    else:
        return "Access Denied: Unauthorized domain"

@app.route('/mac')
def mac():
    return render_template('mac.html')

@app.route('/iphone')
def iphone():
    return render_template('iphone.html')


@app.route('/cart')
def cart():
    user_email = request.args.get('user_email', '')
    # Get the user's cart
    user_cart = carts.get(user_email, [])

    # Calculate grand_total in the Python code (corrected logic)
    grand_total = sum(float(product['price'].replace("₹ ", "").replace(",", "")) for product in user_cart if product['price'])


    # Calculate total quantity in the cart
    total_quantity = sum(product['quantity'] for product in user_cart)
    final_total= "{:,}".format(grand_total*total_quantity)


    return render_template('cart.html', user_cart=user_cart, user_email=user_email, grand_total=grand_total, total_quantity=total_quantity, final_total=final_total)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    user_email = request.form.get('user_email', '')
    product_name = request.form.get('product_name', '')

    # Retrieve the product details
    product_details = {
        'name': request.form.get('product_name', ''),
        'image': request.form.get('product_image', ''),
        'description': request.form.get('product_description', ''),
        'rating': request.form.get('product_rating', ''),
        'price': request.form.get('product_price', ''),
        'quantity': int(request.form.get('quantity', 0)),  # Add quantity information
    }

    # Check if the product is already in the user's cart
    cart = carts.setdefault(user_email, [])
    existing_product = next((p for p in cart if p['name'] == product_name), None)

    if existing_product:
        # Update the quantity if the product is already in the cart
        existing_product['quantity'] += product_details['quantity']
    else:
        # Add the product details to the user's cart
        cart.append(product_details)

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

@app.route('/payment_gateway')  # Add this line
def payment_gateway():
    user_email = request.args.get('user_email', '')
    domain = user_email.split('@')[-1]

    return render_template('payment_gateway.html', domain=domain)
@app.route('/personal-details')  # Corrected route
def personal_details():
    user_email = request.args.get('user_email', '')
    domain = user_email.split('@')[-1]

    return render_template('personal-details.html', domain=domain,  user_email=user_email)




@app.route('/payment-success')
def payment_success():
    user_email = request.args.get('user_email', '')
    domain = user_email.split('@')[-1]

    return render_template('payment-success.html', user_email=user_email, domain=domain)




if __name__ == '__main__':
    app.run(debug=True)
