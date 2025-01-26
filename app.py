from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector
from werkzeug.utils import secure_filename
from mysql.connector import Error
from datetime import datetime
import os
import random
import traceback
import re
# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'mine1234'

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bar_pos_db'

# Function to get the MySQL connection
def get_db_connection():
    connection = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
    return connection


# ----------------------- Authentication Routes ------------------------

@app.route('/')
def index():
    """Home route, redirects based on user role."""
    if 'loggedin' in session:
        if session['role'] == "admin":
            conn = get_db_connection()
    
            # Create a cursor to interact with the database
            cursor = conn.cursor(dictionary=True)

            # Execute SQL query to get total sales for today
            cursor.execute("""
                SELECT 
                    SUM(CASE 
                        WHEN discounted_price IS NOT NULL THEN discounted_price
                        ELSE total_price
                    END) AS total_sales_today
                FROM 
                    sales
                WHERE 
                    DATE(date_updated) = CURDATE();
            """)

            # Fetch the result of the query
            total_sales = cursor.fetchone()

            # Ensure total_sales is not None and has the key 'total_sales_today'
            if total_sales and 'total_sales_today' in total_sales:
                total_sales_today = total_sales['total_sales_today']
            else:
                total_sales_today = 0  # Default to 0 if no data is found

            # Render the template with the sales total and user info
            return render_template('dashboard.html', 
                                   total_sales_today=total_sales_today,
                                   username=session['username'], 
                                   role=session['role'])
        else:
            # Render the dashboard for non-admin users
            return render_template('dashboard.html', 
                                   username=session['username'], 
                                   role=session['role'])
    
    # Redirect to login if not logged in
    return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login route for user authentication."""
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
    
        # Create a cursor to interact with the database
        cursor = conn.cursor(dictionary=True)

        # Check user credentials in the database
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()

        if account:
            # Set session variables
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['role'] = account['role']
            msg = 'Logged in successfully!'
            return redirect(url_for('index'))  # Redirect to index after successful login
        else:
            msg = 'Incorrect username/password!'
    return render_template('user_accounts/login.html', msg=msg)



@app.route('/logout')
def logout():
    """Logout route to clear session and redirect to login page."""
    # Remove session variables
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('role', None)

    # Redirect to login page after logout
    return redirect(url_for('login'))




# Start of customer handling
@app.route('/manage_customer')
def manage_customer():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM customer_list')
    customer = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('customer/manage_customer.html',username=session['username'], customer=customer)


@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form.get('customer_name')
        contact = request.form.get('contact')
        address = request.form.get('address')
        
        # Ensure the form data is filled
        if not name or not contact or not address:
            flash("Please fill out the form!")
            return render_template('customer/add_customer.html',username=session['username'])

        # Check if customer already exists
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM customer_list WHERE name = %s', (name,))
        customer = cursor.fetchone()

        if customer:
            flash("Customer already exists!")
        else:
            # Insert the new customer
            cursor.execute('INSERT INTO customer_list (name, contact, address) VALUES (%s, %s, %s)', 
                           (name, contact, address))
            connection.commit()
            flash("You have successfully registered a customer!")
        
        cursor.close()
        connection.close()
        return render_template('customer/add_customer.html',username=session['username'])
    
    # Handle GET request (no action needed for this part)
    return render_template('customer/add_customer.html',username=session['username'])


@app.route('/edit_customer/<int:customer_id>', methods=['POST', 'GET'])
def edit_customer(customer_id):
    if request.method == 'POST':
        # Get data from the form
        name = request.form['name']
        contact = request.form['contact']
        address = request.form['address']
        loyaltypoints = request.form.get('loyaltypoints')  # Optional field, may be NULL

        try:
            # Create connection and execute the update query
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE customer_list 
                SET name=%s, contact=%s, address=%s, loyaltypoints=%s 
                WHERE CustomerID=%s
            """, (name, contact, address, loyaltypoints, customer_id))
            connection.commit()
            
            # Flash success message
            flash("Customer Data Updated Successfully", "success")
        except Exception as e:
            # Flash error message if any exception occurs
            flash(f"Error: {str(e)}", "danger")
        finally:
            # Close the cursor and connection
            cursor.close()
            connection.close()
            return redirect(url_for('manage_customer'))

    elif request.method == 'GET':
        # Retrieve customer data to pre-fill the form (if needed)
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customer_list WHERE CustomerID = %s", (customer_id,))
        customer = cursor.fetchone()
        cursor.close()
        connection.close()
        
        # If customer exists, render an edit form
        if customer:
            return render_template('customer/edit_customer.html',username=session['username'], customer=customer)
        else:
            flash("Customer not found.", "danger")
            return redirect(url_for('manage_customer'))



@app.route('/delete_customer/<string:get_id>')
def delete_customer(get_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Using a parameterized query to prevent SQL injection
    cursor.execute('DELETE FROM customer_list WHERE CustomerID = %s', (get_id,))
    
    # Commit the transaction to apply the changes
    connection.commit()
    
    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Redirect to the 'manage_customer' route
    return redirect(url_for('manage_customer'))


# End of customer handling

# Category Handle

@app.route('/manage_category')
def manage_category():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Execute the query
    cursor.execute('SELECT * FROM category_list')

    # Fetch all the results
    category = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Render the template and pass the category data
    return render_template('category/manage_category.html',username=session['username'], category=category)



@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        name = request.form.get('name')
        
        if not name:
            flash("Please fill out the form!")
        elif not re.match(r'^[A-Za-z0-9]+$', name):
            flash('Category name must contain only characters and numbers!')
        else:
            # Connect to the database using mysql.connector
           
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            
            try:
                # Check if category already exists
                cursor.execute('SELECT * FROM category_list WHERE name = %s', (name,))
                category = cursor.fetchone()
                
                if category:
                    flash("Category already exists!")
                else:
                    # Insert the new category into the database
                    cursor.execute('INSERT INTO category_list (name) VALUES (%s)', (name,))
                    connection.commit()
                    flash("You have successfully registered a Category!")
            
            except mysql.connector.Error as err:
                flash(f"Error: {err}")
            
            finally:
                cursor.close()
                connection.close()

    return render_template('category/add_category.html')




@app.route('/edit_category/<int:category_id>', methods=['POST', 'GET'])
def edit_category(category_id):
    if request.method == 'POST':
        # Get data from the form
        name = request.form['name']

        try:
            # Create connection and execute the update query
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE category_list
                SET name = %s
                WHERE CategoryID = %s
            """, (name, category_id))
            connection.commit()
            
            # Flash success message
            flash("Category Data Updated Successfully", "success")
        except Exception as e:
            # Flash error message if any exception occurs
            flash(f"Error: {str(e)}", "danger")
        finally:
            # Close the cursor and connection
            cursor.close()
            connection.close()
            return redirect(url_for('manage_category'))

    elif request.method == 'GET':
        # Retrieve category data to pre-fill the form (if needed)
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM category_list WHERE CategoryID = %s", (category_id,))
        category = cursor.fetchone()
        cursor.close()
        connection.close()

        # If category exists, render an edit form
        if category:
            return render_template('category/edit_category.html', username=session['username'], category=category)
        else:
            flash("Category not found.", "danger")
            return redirect(url_for('manage_category'))






@app.route('/delete_category/<string:get_id>')
def delete_cátegory(get_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Using a parameterized query to prevent SQL injection
    cursor.execute('DELETE FROM category_list WHERE CategoryID = %s', (get_id,))
    connection.commit()
    
    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Redirect to the 'manage_customer' route
    return redirect(url_for('manage_category'))




@app.route('/manage_supplier')
def manage_supplier():
    try:
        connection = get_db_connection()
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute('SELECT * FROM supplier_list')
            supplier = cursor.fetchall()
        return render_template('supplier/manage_supplier.html',username=session['username'], supplier=supplier)
    except Exception as e:
        # Handle error and return appropriate response
        print(f"Error: {e}")
        return "An error occurred while fetching supplier data."
    finally:
        if connection:
            connection.close()

@app.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    msg = ''
    if request.method == 'POST':
        supplier_name = request.form.get('supplier_name')
        contact = request.form.get('contact')
        address = request.form.get('address')

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM supplier_list WHERE supplier_name = %s', (supplier_name,))
        category = cursor.fetchone()

        if category:
            flash("Supplier already exists!")
        else:
            cursor.execute('INSERT INTO supplier_list (supplier_name, contact, address) VALUES (%s, %s, %s)', 
                           (supplier_name, contact, address))
            connection.commit()
            flash("You have successfully registered a Supplier!")

        cursor.close()
        connection.close()

    return render_template('supplier/add_supplier.html', username=session['username'],msg=msg)






@app.route('/edit_supplier/<int:supplier_id>', methods=['POST', 'GET'])
def edit_supplier(supplier_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Fetch supplier data using supplier_id
    cursor.execute('SELECT * FROM supplier_list WHERE SupplierID = %s', (supplier_id,))
    supplier = cursor.fetchone()

    if request.method == 'POST':
        # Get the data from the form
        supplier_name = request.form['supplier_name']
        contact = request.form['contact']
        address = request.form['address']

        # Update the supplier data in the database
        cursor.execute('UPDATE supplier_list SET supplier_name=%s, contact=%s, address=%s WHERE SupplierID=%s', 
                       (supplier_name, contact, address, supplier_id))
        connection.commit()

        flash("Supplier Data Updated Successfully")
        return redirect(url_for('manage_supplier'))

    cursor.close()
    connection.close()

    if supplier:
        return render_template('supplier/edit_supplier.html', username=session['username'], supplier=supplier)
    else:
        flash("Supplier not found.", "danger")
        return redirect(url_for('manage_supplier'))





@app.route('/delete_supplier/<string:get_id>')
def delete_supplier(get_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('DELETE FROM supplier_list WHERE SupplierID = %s', (get_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('manage_supplier'))



# End of Supplier Management Routes

@app.route('/manage_products', methods=['GET', 'POST'])
def manage_products():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM product_list order by name')
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('product/manage_product.html',username=session['username'], products=products)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Fetch categories from the database (assuming a separate categories table)
    cursor.execute('SELECT * FROM category_list')  # Replace with the correct table for categories
    categories = cursor.fetchall()
    
    # Generate a random SKU for the product
    random_num = random.randint(1005540, 9978799)  # This will be used as the SKU if not provided by the user
    
    if request.method == 'POST':
        # Retrieve form data
        category_id = request.form.get('category_id')  # Ensure this matches the frontend form field name
        sku = request.form.get('serial_no')  # SKU from form (this should be populated with the random SKU in the frontend)
        price = request.form.get('price')
        name = request.form.get('name')
        description = request.form.get('description')
        quantity = request.form.get('quantity')
        reorder_level = request.form.get('reorder_level')

        # Check if the product already exists with the same SKU and category
        cursor.execute('SELECT * FROM product_list WHERE category_id = %s AND sku = %s', (category_id, sku))
        existing_product = cursor.fetchone()

        if existing_product:
            flash("This product with the same SKU already exists!")
        else:
            # Insert new product into the product_list table
            cursor.execute('INSERT INTO product_list (category_id, sku, price, name, description, quantity, reorder_level) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                           (category_id, sku, price, name, description, quantity, reorder_level))
            connection.commit()
            flash("You have successfully registered a product!")

    cursor.close()
    connection.close()

    # Pass the categories and random SKU to the template
    return render_template('product/add_product.html',random_num=random_num, username=session['username'],categories=categories)


@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Fetch the product data from the database
    cursor.execute('SELECT * FROM product_list WHERE ProductID = %s', (product_id,))
    product = cursor.fetchone()

    if not product:
        flash("Product not found!")
        return redirect(url_for('manage_products'))  # Redirect to a products list page or home

    # Ensure the 'quantity' field is not None or empty, and provide a default if needed
    if product['quantity'] is None:
        product['quantity'] = 0

    # Fetch categories from the database for the dropdown
    cursor.execute('SELECT * FROM category_list')  # Assuming category_list is the name of the category table
    categories = cursor.fetchall()

    if request.method == 'POST':
        # Get the form data
        category_id = request.form.get('category_id')
        sku = request.form.get('serial_no')
        price = request.form.get('price')
        name = request.form.get('name')
        description = request.form.get('description')
        quantity = request.form.get('quantity')
        reorder_level = request.form.get('reorder_level')

        # Convert quantity to an integer (default to 0 if invalid)
        try:
            quantity = int(quantity)
        except ValueError:
            quantity = 0  # Default to 0 if the quantity is invalid

        # Determine the change in quantity
        quantity_change = quantity - product['quantity']  # Updated quantity - current quantity

        # Update the product data in the database
        cursor.execute(''' 
            UPDATE product_list
            SET category_id = %s, sku = %s, price = %s, name = %s, description = %s,
                quantity = %s, reorder_level = %s, updated_at = CURRENT_TIMESTAMP
            WHERE ProductID = %s
        ''', (category_id, sku, price, name, description, quantity, reorder_level, product_id))

        # Add a new log entry to the inventory_logs table
        cursor.execute(''' 
            INSERT INTO inventory_logs (product_id, quantity_change, log_date, reason)
            VALUES (%s, %s, CURRENT_TIMESTAMP, %s)
        ''', (product_id, quantity_change, 'price update'))

        # Commit the transaction
        connection.commit()

        # Show a flash message to the user
        flash("Product updated successfully and inventory log created!")

        # Redirect to the product list page
        return redirect(url_for('manage_products'))  

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Render the edit product page and pass product data and categories for the form
    return render_template('product/edit_product.html', username=session['username'], product=product, categories=categories)




@app.route('/delete_product/<string:get_id>')
def delete_product(get_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('DELETE FROM product_list WHERE ProductID = %s', (get_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('manage_products'))


# Route to restock product
@app.route('/restock_product', methods=['GET', 'POST'])
def restock_product():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        # Retrieve form data
        sku = request.form.get('sku')
        restock_quantity = int(request.form.get('restock_quantity'))

        # Check if the product exists
        cursor.execute('SELECT * FROM product_list WHERE sku = %s', (sku,))
        product = cursor.fetchone()

        if product:
            # Calculate new quantity
            new_quantity = product['quantity'] + restock_quantity

            # Update the product's quantity in the database
            cursor.execute('UPDATE product_list SET quantity = %s WHERE sku = %s', (new_quantity, sku))
            connection.commit()

            # Log the inventory change (restock)
            cursor.execute("""
                INSERT INTO inventory_logs (product_id, quantity_change, reason, log_date)
                VALUES (%s, %s, %s, NOW())
            """, (product['ProductID'], restock_quantity, 'restock'))
            connection.commit()

            # Flash a success message to the user
            flash(f"Product with SKU {sku} has been restocked successfully. New quantity: {new_quantity}.")
        else:
            # Flash an error message if the product does not exist
            flash(f"Product with SKU {sku} does not exist!")

    cursor.close()
    connection.close()

    return render_template('product/restock_product.html',username=session['username'])



@app.route('/sale', methods=['GET'])
def practice():
    try:
        connection = get_db_connection()
        # Create a cursor to execute SQL queries
        cursor = connection.cursor(dictionary=True)

        # Fetch customer and product data
        cursor.execute('SELECT * FROM customer_list')
        customers = cursor.fetchall()

        cursor.execute('SELECT * FROM product_list')
        products = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

    except mysql.connector.Error as e:
        app.logger.error(f"Database error: {e}")
        return "Database error", 500

    return render_template('sales/sale.html', username=session['username'],customers=customers, products=products)


@app.route('/save_sale', methods=['POST'])
def save_sale():
    if request.method == 'POST':
        try:
            # Extract data from the JSON body
            data = request.get_json()
            customer_id = data.get('customer_id')
            items = data.get('cart_items')
            total_price = data.get('total_price')  # Total price before discount
            discounted_price = data.get('discounted_price')  # Total price after discount

            # Validate received data
            if not customer_id or not items:
                return jsonify({'message': 'Missing customer ID or cart items.'}), 400

            # Establish a connection to the MySQL database
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)

            # Start a transaction to ensure consistency
            connection.start_transaction()

            # Insert the sale record (this could be a header record for the sale)
            cursor.execute(
                'INSERT INTO sales_summary (customer_id, total_price, discounted_price) VALUES (%s, %s, %s)',
                (customer_id, total_price, discounted_price)
            )
            sale_id = cursor.lastrowid  # Get the sale ID for the items

            # Insert each item in the cart into the sales items table and update inventory
            for item in items:
                product_id = item.get('product_id')
                price = item.get('price')
                quantity = item.get('quantity')
                discount = item.get('discount')
                total_item_price = item.get('total_price')  # Item's total price before discount
                discounted_item_price = item.get('discounted_price')  # Item's price after discount

                # Validate that price is not None or missing
                if price is None:
                    return jsonify({'message': f'Missing price for product ID {product_id}.'}), 400
                
                # Replace 'N/A' or None discount with 0
                if discount in [None, 'N/A', 'n/a', 'N/a']:
                    discount = 0.00

                # Insert the sale item into the sales table with the sale_id as reference
                cursor.execute(
                    'INSERT INTO sales (ProductID, customer_id, price, discount, qty, total_price, discounted_price) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (product_id, customer_id, price, discount, quantity, total_item_price, discounted_item_price)
                )

                # Update the product stock by subtracting the quantity sold
                cursor.execute(
                    'UPDATE product_list SET quantity = quantity - %s WHERE ProductID = %s',
                    (quantity, product_id)
                )

                # Log the inventory change in the inventory_logs table (negative for sales)
                cursor.execute(""" 
                    INSERT INTO inventory_logs (product_id, quantity_change, reason, log_date)
                    VALUES (%s, %s, %s, NOW())
                """, (product_id, -quantity, 'sale'))

            # Commit the transaction if all operations are successful
            connection.commit()

            # Close cursor and connection
            cursor.close()
            connection.close()

            return jsonify({'message': 'Sale data added and inventory updated successfully!'}), 201

        except Exception as e:
            # Rollback the transaction in case of an error
            connection.rollback()

            # Log the full exception stack trace for debugging
            print("Error:", e)
            print("Stack Trace:", traceback.format_exc())

            return jsonify({'message': 'Error occurred: ' + str(e)}), 400






@app.route('/sales_view', methods=['GET', 'POST'])
def sales_view():
    # Set default values for start and end dates (e.g., today)
    start_date = datetime.now().strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')

    # If dates are submitted via POST, use those dates
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

    # Connect to MySQL
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # SQL query to fetch sales between the start and end dates
    query_sales_details = """
        SELECT 
            s.salesID, 
            p.name AS product_name, 
            c.name AS customer_name,  
            s.price,
            s.discount, 
            s.qty, 
            s.date_updated
        FROM 
            sales s
        INNER JOIN 
            product_list p ON s.ProductID = p.ProductID
        INNER JOIN 
            customer_list c ON s.customer_id = c.CustomerID 
        WHERE 
            DATE(s.date_updated) BETWEEN %s AND %s
    """

    query_sales_sum = """
        SELECT 
            SUM(s.price * s.qty) AS total_sales
        FROM 
            sales s
        INNER JOIN 
            product_list p ON s.ProductID = p.ProductID
        WHERE 
            DATE(s.date_updated) BETWEEN %s AND %s
    """

    query_sales_quantity = """
        SELECT 
            SUM(s.qty) AS total_quantity
        FROM 
            sales s
        INNER JOIN 
            product_list p ON s.ProductID = p.ProductID
        WHERE 
            DATE(s.date_updated) BETWEEN %s AND %s
    """

    # Execute queries with the provided date range
    cursor.execute(query_sales_details, (start_date, end_date))
    sales = cursor.fetchall()

    cursor.execute(query_sales_sum, (start_date, end_date))
    total_sales = cursor.fetchone()['total_sales']

    cursor.execute(query_sales_quantity, (start_date, end_date))
    total_quantity = cursor.fetchone()['total_quantity']

    # Format total_sales and total_quantity with commas
    formatted_total_sales = "{:,.2f}".format(total_sales) if total_sales else '0.00'
    formatted_total_quantity = "{:,}".format(total_quantity) if total_quantity else '0'

    # Close the database connection
    cursor.close()
    conn.close()

    # Render the template with the formatted values
    return render_template('sales/sales_view.html',username=session['username'], 
                           sales=sales, 
                           total_quantity=formatted_total_quantity, 
                           total_sales=formatted_total_sales, 
                           start_date=start_date, 
                           end_date=end_date)



# Function to calculate discount
def calculate_discount(original_price, discounted_price):
    # Calculate the discount amount
    discount_amount = original_price - discounted_price
    # Calculate the discount percentage
    discount_percentage = (discount_amount / original_price) * 100
    return discount_amount, discount_percentage


@app.route('/discount_percentage', methods=['GET', 'POST'])
def discount_percentage():
    if request.method == 'POST':
        try:
            original_price = float(request.form['original_price'])
            discounted_price = float(request.form['discounted_price'])

            if original_price <= 0 or discounted_price < 0:
                raise ValueError("Prices must be positive numbers.")

            discount_amount = original_price - discounted_price
            discount_percentage = (discount_amount / original_price) * 100

            return render_template('sales/discount_percentage.html', username=session['username'],
                                   original_price=original_price, 
                                   discounted_price=discounted_price,
                                   discount_amount=discount_amount,
                                   discount_percentage=discount_percentage)
        except (ValueError, TypeError):
            error = "Please enter valid numeric values."
            return render_template('sales/discount_percentage.html', username=session['username'],error=error)

    return render_template('sales/discount_percentage.html',username=session['username'])



# Define the custom 'date' filter
@app.template_filter('date')
def format_date(value, format='%Y-%m-%d %H:%M:%S'):
    if value is not None:
        return value.strftime(format)
    return value
    




@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            # Insert user data into the database (without password hashing)
            cursor.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)',
                           (username, password, role))
            connection.commit()
            flash('User added successfully!', 'success')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
            app.logger.error(f"Database error: {err}")  # Log error for debugging
        finally:
            cursor.close()
            connection.close()

        return redirect(url_for('index'))  # Redirect to the index page after success
    
    return render_template('user_accounts/add_user.html',username=session['username'])  # Render the form for GET requests





@app.route('/manage_users')
def manage_users():
    # Fetch all non-admin users from the database
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE role != 'admin'")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('user_accounts/manage_users.html',username=session['username'], users=users)




@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        try:
            cursor.execute('UPDATE users SET username = %s, password = %s, role = %s WHERE id = %s',
                           (username, password, role, id))
            connection.commit()
            flash('User updated successfully!', 'success')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.close()
            connection.close()
        
        return redirect(url_for('index'))
    
    cursor.execute('SELECT * FROM users WHERE id = %s', (id,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('user_accounts/edit_user.html', username=session['username'],user=user)

@app.route('/delete_user/<int:id>', methods=['GET'])
def delete_user(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute('DELETE FROM users WHERE id = %s', (id,))
        connection.commit()
        flash('User deleted successfully!', 'success')
    except mysql.connector.Error as err:
        flash(f'Error: {err}', 'danger')
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('index'))
