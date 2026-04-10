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
        description = request.form['description']
        price = float(request.form['price'])
        category_id = int(request.form['category_id'])
        add_inventory_item(description, price, category_id)
        flash('Item added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_user.html')

@app.route('/delete-user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        item_id = int(request.form['item_id'])
        delete_inventory_item(item_id)
        flash('Item deleted successfully!', 'warning')
        return redirect(url_for('home'))
    return render_template('delete_user.html')

@app.route('/display-users')
def display_users():
    users_list = execute_query('SELECT * FROM Inventory')
    return render_template('display_users.html', users=users_list)


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

@app.route('/update-order', methods=['GET', 'POST'])
def update_order_route():
    if request.method == 'POST':
        order_id = request.form['order_id']
        quantity = int(request.form['quantity'])
        update_order(order_id, quantity)
        flash('Order updated!', 'success')
        return redirect(url_for('inbound_inv'))
    return render_template('update_order.html')

# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)