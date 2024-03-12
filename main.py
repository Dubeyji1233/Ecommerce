import pandas as pd
from flask import Flask, render_template, redirect, url_for,request,render_template_string,session
from flask_mail import Mail
import csv
import smtplib
from urllib.parse import quote
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import io,os
import chardet

from pandas import read_excel

app = Flask(__name__, template_folder='templates')
mail = Mail(app)

# Mock product data for different domains
products = {
    'orientindia.net': 'Orient India Products',
    'amazon.in': 'Amazon India Products',
    'apple.in': 'Apple India Products',
    'apple.com': 'Apple Products'
}

# Initialize an empty cart for each user
carts = {}
def read_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)
    return data


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
        if domain == 'apple.in':
            return render_template('orient.html', user_products=user_products, user_email=user_email)
        elif domain == 'amazon.in':
            return render_template('amazon.html', user_products=user_products, user_email=user_email)
        elif domain in ['orientindia.net', 'apple.com']:
            return render_template('apple.html', user_products=user_products, user_email=user_email)

    else:
        return "Access Denied: Unauthorized domain"


@app.route('/mac')
def mac():
    user_email = request.args.get('user_email', '')
    domain = user_email.split('@')[-1]

    # print(f"User Email: {user_email}")
    # print(f"Domain: {domain}")

    file_path = r'C:\Users\abhishekdubey\PycharmProjects\E-commerce\Product_data\mac1.csv'
    product_data = pd.read_csv(file_path, encoding='ISO-8859-1')
    product_data['Offer Price'] = product_data['Offer Price'].str.replace(',', '')
    # Iterate over DataFrame rows using iterrows()
    products_filtered = [row for index, row in product_data.iterrows() if row['Offer Price'] is not None]

    return render_template('mac.html', user_products=products_filtered, domain=domain, user_email=user_email)

@app.route('/watch')
def watch():
    user_email = request.args.get('user_email', '')
    domain = user_email.split('@')[-1]

    # print(f"User Email: {user_email}")
    # print(f"Domain: {domain}")

    file_path = r'C:\Users\abhishekdubey\PycharmProjects\E-commerce\Product_data\mac1.csv'
    product_data = pd.read_csv(file_path, encoding='ISO-8859-1')
    product_data['Offer Price'] = product_data['Offer Price'].str.replace(',', '')
    # Iterate over DataFrame rows using iterrows()
    products_filtered = [row for index, row in product_data.iterrows() if row['Offer Price'] is not None]

    return render_template('watch.html', user_products=products_filtered, domain=domain, user_email=user_email)

@app.route('/ipad')
def ipad():
    user_email = request.args.get('user_email', '')
    domain = user_email.split('@')[-1]

    # print(f"User Email: {user_email}")
    # print(f"Domain: {domain}")

    file_path = r'C:\Users\abhishekdubey\PycharmProjects\E-commerce\Product_data\mac1.csv'
    product_data = pd.read_csv(file_path, encoding='ISO-8859-1')
    product_data['Offer Price'] = product_data['Offer Price'].str.replace(',', '')
    # Iterate over DataFrame rows using iterrows()
    products_filtered = [row for index, row in product_data.iterrows() if row['Offer Price'] is not None]

    return render_template('ipad.html', user_products=products_filtered, domain=domain, user_email=user_email)


# @app.route('/iphone')
# def iphone():
#     user_email = request.args.get('user_email', '')
#     domain = user_email.split('@')[-1]
#
#     file_path = r'C:\Users\abhishekdubey\PycharmProjects\E-commerce\Product_data\Smart_EPP_Generic_iphone.csv'
#     product_data = pd.read_csv(file_path, encoding='ISO-8859-1')
#     product_data['Offer Price'] = product_data['Offer Price'].str.replace(',', '')
#
#     # Iterate over DataFrame rows using iterrows()
#     products_filtered = [row for index, row in product_data.iterrows() if row['Offer Price'] is not None]
#     # Get unique values from the "Variant" column
#     unique_variants = product_data['Variant'].unique()
#     unique_models = product_data['Model'].unique()
#     unique_colours = product_data['Colour'].unique()
#
#     # Assuming you have unique_models, unique_variants, and unique_colours lists
#     return render_template('iphone.html', user_products=products_filtered, user_models=unique_models, user_variants=unique_variants,
#                            user_colours=unique_colours)

@app.route('/iphone')
def iphone():
    user_email = request.args.get('user_email', '')
    domain = user_email.split('@')[-1]

    file_path = r'C:\Users\abhishekdubey\PycharmProjects\E-commerce\Product_data\Smart_EPP_Generic_iphone.csv'
    product_data = pd.read_csv(file_path, encoding='ISO-8859-1')
    product_data['Offer Price'] =  product_data['Offer Price'].str.replace(',', '')
    # Iterate over DataFrame rows using iterrows()
    products_filtered = [row for index, row in product_data.iterrows() if row['Offer Price'] is not None]

    return render_template('iphone.html', user_products=products_filtered, domain=domain, user_email=user_email)
@app.route('/cart')
def cart():
    user_email = request.args.get('user_email', '')
    price = request.args.get('product_price', '')
    # Get the user's cart
    user_cart = carts.get(user_email, [])
    product = carts.get(price, [])

    # Calculate grand_total in the Python code (corrected logic)
    grand_total = sum(float(product['price'].replace("₹ ", "").replace(',', '')) * product['quantity'] for product in user_cart)

    # Calculate total quantity in the cart
    total_quantity = sum(product['quantity'] for product in user_cart)

    # Format grand_total with comma separator
    formatted_grand_total = "{:,.2f}".format(grand_total)

    return render_template('cart.html', user_cart=user_cart, user_email=user_email, product=product,price=price)

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
        'quantity': int(request.form.get('quantity', 0)),
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

    # Redirect to the product page or any other appropriate page
    return redirect(url_for('index', user_email=user_email, user_cart=cart))

@app.route('/add_to_cart4', methods=['POST'])
def add_to_cart4():
    user_email = request.form.get('user_email', '')
    product_name = request.form.get('product_name', '')
    product_variant = request.form.get('product_variant', '')
    product_colour = request.form.get('product_colour', '')
    product_price = request.form.get('product_price', '')
    product_Key = request.form.get('product_Key', '')
    product_camera = request.form.get('product_camera', '')
    product_image = request.form.get('product_image', '')
    product_chipset = request.form.get('product_chipset', '')
    product_display = request.form.get('product_display', '')

    # Retrieve the product details
    product_details = {
        'name': product_name,
        'variant': product_variant,
        'colour': product_colour,
        'key': f'{product_Key}_{product_name}',  # Include product type in the key
        'camera': product_camera,
        'image': product_image,
        'price': product_price,
        'display': product_display,
        'chipset': product_chipset,
        'quantity': int(request.form.get('quantity', 0)),
    }

    # Check if the product is already in the user's cart
    cart = carts.setdefault(user_email, [])
    existing_product = next((p for p in cart if p['key'] == product_Key), None)

    if existing_product:
        # Update the quantity if the product is already in the cart
        existing_product['quantity'] += product_details['quantity']
    else:
        # Add the product details to the user's cart
        cart.append(product_details)

    # Redirect to the product page or any other appropriate page
    return redirect(url_for('mac', user_email=user_email, user_cart=cart))


@app.route('/add_to_cart1', methods=['POST'])
def add_to_cart1():
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

    # Render the current template with updated cart information
    return render_template('amazon.html', user_email=user_email, user_cart=cart)

@app.route('/add_to_cart2', methods=['POST'])
def add_to_cart2():
    user_email = request.form.get('user_email', '')
    product_name = request.form.get('product_name', '')
    product_variant = request.form.get('product_variant', '')
    product_colour = request.form.get('product_colour', '')
    product_price = request.form.get('product_price', '')
    product_Key = request.form.get('product_Key', '')
    product_camera = request.form.get('product_camera', '')
    product_image= request.form.get('product_image', '')
    product_chipset = request.form.get('product_chipset', '')
    product_display =request.form.get('product_display', '')

    # Retrieve the product details
    product_details = {
        'name': product_name,
        'variant': product_variant,
        'colour': product_colour,
        'key': f'{product_Key}_{product_name}',  # Include product type in the key
        'camera': product_camera,
        'image': product_image,
        'price': product_price,
        'display': product_display,
        'chipset': product_chipset,
        'quantity': int(request.form.get('quantity', 0)),
    }

    # Check if the product is already in the user's cart
    cart = carts.setdefault(user_email, [])
    existing_product = next((p for p in cart if p['key'] == product_Key), None)


    if existing_product:
        # Update the quantity if the product is already in the cart
        existing_product['quantity'] += product_details['quantity']
    else:
        # Add the product details to the user's cart
        cart.append(product_details)

    # Redirect to the product page or any other appropriate page
    return redirect(url_for('iphone', user_email=user_email, user_cart=cart))


@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    user_email = request.form.get('user_email', '')
    product_key = request.form.get('product_key', '')

    # Remove the product from the user's cart
    if user_email in carts:
        updated_cart = [product for product in carts[user_email] if product['key'] != product_key]
        carts[user_email] = updated_cart

    # Redirect back to the cart page
    return redirect(url_for('cart', user_email=user_email))

@app.route('/product_details')
def product_details():
    user_email = request.args.get('user_email', '')
    product_name = request.args.get('product_name', '')
    product_type = request.args.get('product_type', '')

    product_details = get_product_details_by_key(product_name, product_type)


    return render_template('product-details.html', user_email=user_email, product_details=product_details)

def get_product_details_by_key(product_key, product_type):
    file_paths = {
        'mac': r'C:\Users\abhishekdubey\PycharmProjects\E-commerce\Product_data\mac1.csv',
        'iphone': r'C:\Users\abhishekdubey\PycharmProjects\E-commerce\Product_data\Smart_EPP_Generic_iphone.csv'
        # Add other product types as needed
    }

    # Check if the provided product type is in the mapping
    if product_type in file_paths:
        file_path = file_paths[product_type]
        product_details = None

        with open(file_path, 'r', encoding='ISO-8859-1') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if row['Key'] == product_key:
                    product_details = {
                        'name': row['Model'],
                        'variant': row['Variant'],
                        'mrp': row['MRP'],
                        'price': row['Offer Price'],
                        'camera': row['Camera'],
                        'chipset': row['Chipset'],
                        'display': row['Display'],
                        'colour': row['Colour'],
                        'image': row['Image']
                    }
                    break

        return product_details
    else:
        # Handle the case where the provided product type is not in the mapping
        return None

@app.route('/personal-details')
def personal_details():
    user_email = request.args.get('user_email', '')
    domain = user_email.split('@')[-1]

    # Retrieve product details from the user's cart
    user_cart = carts.get(user_email, [])

    return render_template('personal-details.html', domain=domain, user_email=user_email, user_cart=user_cart)

@app.route("/invoice_details", methods=["GET"])
def invoice_details():
    user_email = request.args.get('user_email', '')
    print(user_email)
    first_name = request.args.get('fname', '')
    print(first_name)
    last_name = request.args.get('lname', '')
    print(last_name)
    employee_code = request.args.get('ecode', '')
    print(employee_code)
    company_name = request.args.get('cname', '')
    print(company_name)
    phone_number = request.args.get('nnumber', '')  # Assuming the input type is 'tel'
    print(phone_number)
    email_address = request.args.get('mail', '')  # Assuming the input type is 'email'
    print(email_address)
    country = request.args.get('selection', '')
    print(country)
    house_address = request.args.get('houseadd', '')
    print(house_address)
    apartment = request.args.get('apartment', '')
    print(apartment)
    city = request.args.get('city', '')
    print(city)
    state = request.args.get('state', '')
    print(state)

    user_cart = carts.get(user_email, [])

    return send_invoice_mail(user_email=user_email, user_cart=user_cart, first_name=first_name, last_name=last_name,
                             employee_code=employee_code, company_name=company_name, phone_number=phone_number,
                             email_address=email_address, country=country, house_address=house_address,
                             apartment=apartment, city=city, state=state)

@app.route("/send_invoice_mail", methods=["GET"])
def send_invoice_mail(user_email, user_cart, first_name, last_name, employee_code, company_name, phone_number,
                      email_address, country, house_address, apartment, city, state):
    if not user_email:
        return 'Invalid recipient email address'

    msg = MIMEMultipart()
    msg['From'] = 'abhishekoffical30@gmail.com'
    msg['To'] = 'shubhambhoite@orientindia.net'
    msg['Subject'] = 'Invoice Details'

    body = f'Dear Shubham,<br><br>'
    body += f'{first_name} {last_name} order has been placed successfully Please Give Approvel.<br><br>'
    body += 'Ordered Items:<br>'

    grand_total = 0
    total_quantity = 0

    for item in user_cart:
        body += f'<img src="{item["image"]}" alt="{item["name"]}" style="max-width: 100px; max-height: 100px;"> ' \
                f'x {item["name"]} x {item["quantity"]}<br>'

        total = float(item["price"].replace("₹ ", "").replace(',', '')) * item['quantity']
        grand_total += total
        total_quantity += item['quantity']

        body += f'Total for {item["name"]}: {total}<br><br>'

    # Display Total Quantity and Grand Total
    body += f'Total Quantity: {total_quantity}<br>'
    body += f'Grand Total: {grand_total}<br><br>'
    body += '<br>Order Details<br><br>'
    body += f'Employee Code: {employee_code}<br>'
    body += f'Company Name: {company_name}<br>'
    body += f'Phone Number: {phone_number}<br>'
    body += f'Email Address: {email_address}<br>'
    body += f'Country: {country}<br>'
    body += f'Street Address: {house_address}, {apartment}<br>'
    body += f'City: {city}<br>'
    body += f'State: {state}<br><br><br><br>'

    # approval_link = f'http://127.0.0.1:5000/Approve_invoice_mail?user_email={user_email}&fname={first_name}&lname={last_name}&ecode={employee_code}&cname={company_name}&nnumber={phone_number}&country={country}&address={house_address}&city={city}&state={state}'
    # cancellation_link = f'http://127.0.0.1:5000/cancel_invoice/{quote(user_email)}/{quote(first_name)}/{quote(last_name)}/{grand_total}/{employee_code}/{quote(phone_number)}/{quote(email_address)}/{quote(country)}/{quote(house_address)}'
    # approval_link = f'http://127.0.0.1:5000/approve_invoice/{quote(user_email)}/{quote(first_name)}/{quote(last_name)}/{grand_total}/{employee_code}/{quote(phone_number)}/{quote(email_address)}/{quote(country)}/{quote(house_address)}'
    body += f'''
            <p>Please approve or cancel the request:</p>
            <a href="http://127.0.0.1:5000/Approve_invoice_mail?user_email={user_email}&fname={first_name}&lname={last_name}&ecode={employee_code}&cname={company_name}&nnumber={phone_number}&country={country}&address={house_address}&city={city}&state={state}" style="padding: 10px; background-color: #4CAF50; color: white; text-decoration: none;">Approve</a>
            <br>
            <br>
            <br>
            <a href="http://127.0.0.1:5000/cancel_invoice_mail?user_email={user_email}&fname={first_name}&lname={last_name}&ecode={employee_code}&cname={company_name}&nnumber={phone_number}&country={country}&address={house_address}&city={city}&state={state}" style="padding: 10px; background-color: #FF0000; color: white; text-decoration: none;">Cancel</a>
        '''


    msg.attach(MIMEText(body.encode('utf-8'), 'html', 'ISO-8859-1'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('abhishekoffical30@gmail.com', '')
        server.sendmail('abhishekoffical30@gmail.com', 'shubhambhoite@orientindia.net', msg.as_string())
    print('Mail Send to Manager')

@app.route("/Approve_invoice_mail", methods=["GET"])
def Approve_invoice_mail():
    user_email = request.args.get('user_email', '')
    print(user_email)
    first_name = request.args.get('fname', '')
    last_name = request.args.get('lname', '')
    employee_code = request.args.get('ecode', '')
    company_name = request.args.get('cname', '')
    phone_number = request.args.get('nnumber', '')
    email_address = request.args.get('mail', '')
    country = request.args.get('country', '')
    house_address = request.args.get('address', '')
    city = request.args.get('city', '')
    state = request.args.get('state', '')

    user_cart = carts.get(user_email, [])
    if not user_email:
        return 'Invalid recipient email address'

    msg = MIMEMultipart()
    msg['From'] = 'abhishekoffical30@gmail.com'
    msg['To'] = user_email
    msg['Subject'] = 'Invoice Details'

    body = f'Dear {first_name} {last_name},<br><br>'
    body += 'Thank you for shopping with us. Your order has been placed successfully.<br><br>'
    body += 'Ordered Items:<br>'

    grand_total = 0
    total_quantity = 0

    for item in user_cart:
        body += f'<img src="{item["image"]}" alt="{item["name"]}" style="max-width: 100px; max-height: 100px;"> ' \
                f'x {item["name"]} x {item["quantity"]}<br>'

        total = float(item["price"].replace("₹ ", "").replace(',', '')) * item['quantity']
        grand_total += total
        total_quantity += item['quantity']

        body += f'Total for {item["name"]}: {total}<br><br>'

    # Display Total Quantity and Grand Total
    body += f'Total Quantity: {total_quantity}<br>'
    body += f'Grand Total: {grand_total}<br><br>'
    body += '<br>Order Details<br><br>'
    body += f'Employee Code: {employee_code}<br>'
    body += f'Phone Number: {phone_number}<br>'
    body += f'Email Address: {email_address}<br>'
    body += f'Country: {country}<br>'
    body += f'Street Address: {house_address}<br>'

    msg.attach(MIMEText(body.encode('utf-8'), 'html', 'ISO-8859-1'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('abhishekoffical30@gmail.com', '')
        server.sendmail('abhishekoffical30@gmail.com', user_email, msg.as_string())

    print('Order has been approved by the Manager')
    return render_template('login.html',user_email=user_email, action='approved')


@app.route("/cancel_invoice_mail", methods=["GET"])
def cancel_invoice_mail():
    user_email = request.args.get('user_email', '')
    first_name = request.args.get('fname', '')
    last_name = request.args.get('lname', '')

    user_cart = carts.get(user_email, [])

    if not user_email:
        return 'Invalid recipient email address'

    msg = MIMEMultipart()
    msg['From'] = 'abhishekoffical30@gmail.com'
    msg['To'] = user_email
    msg['Subject'] = 'Order Cancellation Confirmation'

    body = f'Dear {first_name} {last_name},<br><br>'
    body += 'We regret to inform you that your order has been cancelled.<br><br>'
    grand_total = 0
    total_quantity = 0

    for item in user_cart:
        body += f'<img src="{item["image"]}" alt="{item["name"]}" style="max-width: 100px; max-height: 100px;"> ' \
                f'x {item["name"]} x {item["quantity"]}<br>'

        total = float(item["price"].replace("₹ ", "").replace(',', '')) * item['quantity']
        grand_total += total
        total_quantity += item['quantity']

        body += f'Total for {item["name"]}: {total}<br><br>'

    # Display Total Quantity and Grand Total
    body += f'Total Quantity: {total_quantity}<br>'
    body += f'Grand Total: {grand_total}<br><br>'

    body += 'If you have any questions or concerns, please contact our customer support team.<br><br>'

    msg.attach(MIMEText(body.encode('utf-8'), 'html', 'ISO-8859-1'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('abhishekoffical30@gmail.com', '')
        server.sendmail('abhishekoffical30@gmail.com', user_email, msg.as_string())
    print('Order has been cancel by the Manager')
    return render_template('login.html', user_email=user_email, action='canceled')


if __name__ == "__main__":
    app.run(debug=True)




# @app.route("/approve_Order", methods=["GET"])
# def approve_Order(user_email, user_cart, first_name, last_name, employee_code, company_name, phone_number,
#                       email_address, country, house_address, apartment, city, state):
#
#
#     if not user_email:
#         return 'Invalid recipient email address'
#
#     msg = MIMEMultipart()
#     msg['From'] = 'abhishekoffical30@gmail.com'
#     msg['To'] = 'abhishekoffical30@gmail.com'
#     msg['Subject'] = 'Invoice Details'
#
#     body = f'Dear Shubham,<br><br>'
#     body += f'{first_name} {last_name} order has been placed successfully Please Give Approvel.<br><br>'
#     body += 'Ordered Items:<br>'
#
#     grand_total = 0
#     total_quantity = 0
#
#     for item in user_cart:
#         body += f'<img src="{item["image"]}" alt="{item["name"]}" style="max-width: 100px; max-height: 100px;"> ' \
#                 f'x {item["name"]} x {item["quantity"]}<br>'
#
#         total = float(item["price"].replace("₹ ", "").replace(',', '')) * item['quantity']
#         grand_total += total
#         total_quantity += item['quantity']
#
#         body += f'Total for {item["name"]}: {total}<br><br>'
#
#     # Display Total Quantity and Grand Total
#     body += f'Total Quantity: {total_quantity}<br>'
#     body += f'Grand Total: {grand_total}<br><br>'
#     body += '<br>Order Details<br><br>'
#     body += f'Employee Code: {employee_code}<br>'
#     body += f'Company Name: {company_name}<br>'
#     body += f'Phone Number: {phone_number}<br>'
#     body += f'Email Address: {email_address}<br>'
#     body += f'Country: {country}<br>'
#     body += f'Street Address: {house_address}, {apartment}<br>'
#     body += f'City: {city}<br>'
#     body += f'State: {state}<br><br><br><br>'
# body += f'''
#                 <p>Please approve or cancel the request:</p>
#                 <a href="http://127.0.0.1:5000/Approve_invoice_mail?user_email={user_email}&fname={first_name}&lname={last_name}&ecode={employee_code}&cname={company_name}&nnumber={phone_number}&country={country}&address={house_address}&city={city}&state={state}" style="padding: 10px; background-color: #4CAF50; color: white; text-decoration: none;">Approve</a>
#                 <br>
#                 <br>
#                 <br>
#                 <a href="http://127.0.0.1:5000/cancel_invoice_mail?user_email={user_email}&fname={first_name}&lname={last_name}&ecode={employee_code}&cname={company_name}&nnumber={phone_number}&country={country}&address={house_address}&city={city}&state={state}" style="padding: 10px; background-color: #FF0000; color: white; text-decoration: none;">Cancel</a>
#             '''
#
#
#     msg.attach(MIMEText(body.encode('utf-8'), 'html', 'ISO-8859-1'))
#
#     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
#         server.login('abhishekoffical30@gmail.com', '')
#         server.sendmail('abhishekoffical30@gmail.com', 'abhishekoffical30@gmail.com', msg.as_string())
#
#     print('Mail Send to Manager')
#
#
# @app.route("/Approve_invoice_mail", methods=["GET"])
# def Approve_invoice_mail():
#     user_email = request.args.get('user_email', '')
#     print(user_email)
#     first_name = request.args.get('fname', '')
#     last_name = request.args.get('lname', '')
#     employee_code = request.args.get('ecode', '')
#     company_name = request.args.get('cname', '')
#     phone_number = request.args.get('nnumber', '')
#     email_address = request.args.get('mail', '')
#     country = request.args.get('selection', '')
#     house_address = request.args.get('houseadd', '')
#     apartment = request.args.get('apartment', '')
#     city = request.args.get('city', '')
#     state = request.args.get('state', '')
#
#     user_cart = carts.get(user_email, [])
#
#     if not user_email:
#         return 'Invalid recipient email address'
#
#     msg = MIMEMultipart()
#     msg['From'] = 'abhishekoffical30@gmail.com'
#     msg['To'] = user_email
#     msg['Subject'] = 'Invoice Details'
#
#     body = f'Dear {first_name} {last_name},<br><br>'
#     body += 'Thank you for shopping with us. Your order has been placed successfully.<br><br>'
#     body += 'Ordered Items:<br>'
#
#     grand_total = 0
#     total_quantity = 0
#
#     for item in user_cart:
#         body += f'<img src="{item["image"]}" alt="{item["name"]}" style="max-width: 100px; max-height: 100px;"> ' \
#                 f'x {item["name"]} x {item["quantity"]}<br>'
#
#         total = float(item["price"].replace("₹ ", "").replace(',', '')) * item['quantity']
#         grand_total += total
#         total_quantity += item['quantity']
#
#         body += f'Total for {item["name"]}: {total}<br><br>'
#
#     # Display Total Quantity and Grand Total
#     body += f'Total Quantity: {total_quantity}<br>'
#     body += f'Grand Total: {grand_total}<br><br>'
#
#     body += '<br>Order Details<br><br>'
#     body += f'Employee Code: {employee_code}<br>'
#     body += f'Company Name: {company_name}<br>'
#     body += f'Phone Number: {phone_number}<br>'
#     body += f'Email Address: {email_address}<br>'
#     body += f'Country: {country}<br>'
#     body += f'Street Address: {house_address}, {apartment}<br>'
#     body += f'City: {city}<br>'
#     body += f'State: {state}<br>'
#
#     msg.attach(MIMEText(body.encode('utf-8'), 'html', 'ISO-8859-1'))
#
#     with smtplib.SMTP('smtp.gmail.com', 587) as server:
#         server.starttls()
#         server.login('abhishekoffical30@gmail.com', '')
#         server.sendmail('abhishekoffical30@gmail.com', user_email, msg.as_string())
#
#     print('Order has been approved by the Manager')
#     return render_template('login.html',user_email=user_email, action='approved')
#
#
# @app.route("/cancel_invoice_mail", methods=["GET"])
# def cancel_invoice_mail():
#     user_email = request.args.get('user_email', '')
#     first_name = request.args.get('fname', '')
#     last_name = request.args.get('lname', '')
#
#     user_cart = carts.get(user_email, [])
#     if not user_email:
#         return 'Invalid recipient email address'
#
#     msg = MIMEMultipart()
#     msg['From'] = 'abhishekoffical30@gmail.com'
#     msg['To'] = user_email
#     msg['Subject'] = 'Order Cancellation Confirmation'
#
#     body = f'Dear {first_name} {last_name},<br><br>'
#     body += 'We regret to inform you that your order has been cancelled.<br><br>'
#     grand_total = 0
#     total_quantity = 0
#
#     for item in user_cart:
#         body += f'<img src="{item["image"]}" alt="{item["name"]}" style="max-width: 100px; max-height: 100px;"> ' \
#                 f'x {item["name"]} x {item["quantity"]}<br>'
#
#         total = float(item["price"].replace("₹ ", "").replace(',', '')) * item['quantity']
#         grand_total += total
#         total_quantity += item['quantity']
#
#         body += f'Total for {item["name"]}: {total}<br><br>'
#
#     # Display Total Quantity and Grand Total
#     body += f'Total Quantity: {total_quantity}<br>'
#     body += f'Grand Total: {grand_total}<br><br>'
#
#     body += 'If you have any questions or concerns, please contact our customer support team.<br><br>'
#
#     msg.attach(MIMEText(body.encode('utf-8'), 'html', 'ISO-8859-1'))
#
#     with smtplib.SMTP('smtp.gmail.com', 587) as server:
#         server.starttls()
#         server.login('abhishekoffical30@gmail.com', '')
#         server.sendmail('abhishekoffical30@gmail.com', user_email, msg.as_string())
#     print('Order has been cancel by the Manager')
#     return render_template('login.html', user_email=user_email, action='canceled')



# @app.route("/approve_Order", methods=["GET"])
# def approve_Order(user_email, user_cart, first_name, last_name, employee_code, company_name, phone_number,
#                       email_address, country, house_address, apartment, city, state):
#     if not user_email:
#         return 'Invalid recipient email address'
#
#     msg = MIMEMultipart()
#     msg['From'] = 'abhishekoffical30@gmail.com'
#     msg['To'] = user_email
#     msg['Subject'] = 'Invoice Details'
#
#     body = f'Dear Shubham,<br><br>'
#     body += f'{first_name} {last_name} order has been placed successfully Please Give Approvel.<br><br>'
#     body += 'Ordered Items:<br>'
#
#     grand_total = 0
#     total_quantity = 0
#
#     for item in user_cart:
#         body += f'<img src="{item["image"]}" alt="{item["name"]}" style="max-width: 100px; max-height: 100px;"> ' \
#                 f'x {item["name"]} x {item["quantity"]}<br>'
#
#         total = float(item["price"].replace("₹ ", "").replace(',', '')) * item['quantity']
#         grand_total += total
#         total_quantity += item['quantity']
#
#         body += f'Total for {item["name"]}: {total}<br><br>'
#
#     # Display Total Quantity and Grand Total
#     body += f'Total Quantity: {total_quantity}<br>'
#     body += f'Grand Total: {grand_total}<br><br>'
#
#     body += '<br>Order Details<br><br>'
#     body += f'Employee Code: {employee_code}<br>'
#     body += f'Company Name: {company_name}<br>'
#     body += f'Phone Number: {phone_number}<br>'
#     body += f'Email Address: {email_address}<br>'
#     body += f'Country: {country}<br>'
#     body += f'Street Address: {house_address}, {apartment}<br>'
#     body += f'City: {city}<br>'
#     body += f'State: {state}<br><br><br><br>'
#
#     msg.attach(MIMEText(body.encode('utf-8'), 'html', 'ISO-8859-1'))
#
#     with smtplib.SMTP('smtp.gmail.com', 587) as server:
#         server.starttls()
#         server.login('abhishekoffical30@gmail.com', '')
#         server.sendmail('abhishekoffical30@gmail.com', user_email, msg.as_string())
