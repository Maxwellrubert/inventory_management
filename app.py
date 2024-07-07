from flask import Flask, render_template, redirect, url_for, request
from forms import ProductForm
from models import Product
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object('config')

# MySQL configurations
app.config['MYSQL_USER'] = app.config['MYSQL_DATABASE_USER']
app.config['MYSQL_PASSWORD'] = app.config['MYSQL_DATABASE_PASSWORD']
app.config['MYSQL_DB'] = app.config['MYSQL_DATABASE_DB']
app.config['MYSQL_HOST'] = app.config['MYSQL_DATABASE_HOST']

mysql = MySQL(app)

# Ensure Product class uses the mysql instance defined here
Product.mysql = mysql

@app.route('/')
def index():
    products = Product.get_all()
    return render_template('products.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        Product.add(form.name.data, form.quantity.data, form.price.data)
        return redirect(url_for('index'))
    return render_template('add_product.html', form=form)

@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.get_by_id(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        Product.update(product_id, form.name.data, form.quantity.data, form.price.data)
        return redirect(url_for('index'))
    return render_template('edit_product.html', form=form, product_id=product_id)

@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    Product.delete(product_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)