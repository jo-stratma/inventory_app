import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask import Flask, request, redirect, url_for, render_template, flash


app = Flask(__name__)
app.secret_key = 'test_ahtglobal'

# Docker
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@mysql/inventory_db'
# local

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'


db = SQLAlchemy(model_class=Base)
# initialize the app with the extension
db.init_app(app)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    order_number = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Integer, nullable=False)
    manufacturer = db.Column(db.String(100), nullable=True)
    link = db.Column(db.String(100), nullable=True)
    amount = db.Column(db.Integer, nullable=False)


with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Get all items from the database
    items = Inventory.query.all()
    # Show the items on the index page
    return render_template('index.html', items=items)


@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        # Get data from the form
        id = request.form['id']
        name = request.form['name']
        location = request.form['location']
        order_number = request.form['order_number']
        date = request.form['date']
        manufacturer = request.form['manufacturer']
        link = request.form['link']
        amount = request.form['amount']





        # Create a new item and save it to the database
        new_item = Inventory(
            id = id, name = name, location = location, order_number = order_number, date = date,
            manufacturer = manufacturer, link = link, amount = amount )
        db.session.add(new_item)
        db.session.commit()
        flash('Item added successfully!')
        # Redirect to the main page
        return redirect(url_for('index'))

    # Show the form to add a new item
    return render_template('add.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    # Get the item we want to edit
    item = Inventory.query.get(id)
    if request.method == 'POST':
        # Update the item's details with the form data
        item.name = request.form['name']
        item.price = request.form['price']
        item.mac_address = request.form['mac_address']
        item.serial_number = request.form['serial_number']
        item.manufacturer = request.form['manufacturer']
        item.description = request.form['description']

        # Save the updated item to the database
        db.session.commit()
        flash('Item updated successfully!')
        # Redirect to the main page
        return redirect(url_for('index'))

    # Show the form to edit the item
    return render_template('edit.html', item=item)


@app.route('/delete/<int:id>')
def delete_item(id):
    # Get the item we want to delete
    item = Inventory.query.get(id)
    # Remove the item from the database
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully!')
    # Redirect to the main page
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Run the app with debug mode on
    app.run(debug=True)
