# author: T. Urness and M. Moore
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT

from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        genre = request.form['genre']
        
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("Name:", name, ":", "Favorite Genre:", genre)
        
        flash('User added successfully! Huzzah!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('add_user.html')

@app.route('/delete-user',methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("Name to delete:", name)
        
        flash('User deleted successfully! Hoorah!', 'warning') 
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('delete_user.html')


@app.route('/display-users')
def display_users():
    users_list = execute_query('SELECT * FROM Inventory')
    return render_template('display_users.html', users=users_list)


# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

@app.route('/inbound-orders')
def inbound_inv():
    orders = get_all_orders()
    return render_template('inbound_inv.html', orders=orders)

@app.route('/add-order', methods=['GET', 'POST'])
def add_order_route():
    if request.method == 'POST':
        order_id = request.form['order_id']
        item_description = request.form['item_description']
        quantity = int(request.form['quantity'])
        supplier = request.form['supplier']
        add_order(order_id, item_description, quantity, supplier)
        flash('Order added successfully!', 'success')
        return redirect(url_for('inbound_inv'))
    return render_template('add_order.html')

@app.route('/delete-order', methods=['GET', 'POST'])
def delete_order_route():
    if request.method == 'POST':
        order_id = request.form['order_id']
        delete_order(order_id)
        flash('Order deleted!', 'warning')
        return redirect(url_for('inbound_inv'))
    return render_template('delete_order.html')

@app.route('/inventory-by-category')
def inventory_by_category():
    results = execute_query('''
        SELECT Inventory.description, Inventory.price, Category.name 
        FROM Inventory 
        JOIN Category ON Inventory.categoryID = Category.categoryID
    ''')
    return render_template('inventory_by_category.html', items=results)