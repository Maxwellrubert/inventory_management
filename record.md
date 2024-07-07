Here's a structured format for your record notebook for the Inventory Management project using MySQL and Flask:

### Title
**Inventory Management System Using Flask and MySQL**

### Aim
To develop a web-based inventory management system using the Flask framework and MySQL database, allowing users to manage product inventory, including adding, updating, and deleting products, and viewing product details.

### Procedure

#### 1. **Project Setup**

1. **Install Flask and MySQL Client:**
   ```bash
   pip install flask flask-mysql flask-wtf
   ```

2. **Create a Flask Project Structure:**
   ```bash
   inventory_management/
   ├── app.py
   ├── config.py
   ├── templates/
   │   ├── base.html
   │   ├── add_product.html
   │   ├── edit_product.html
   │   └── products.html
   ├── static/
   │   └── styles.css
   ├── forms.py
   ├── models.py
   └── requirements.txt
   ```

#### 2. **Set Up MySQL Database**

1. **Install MySQL Server** (if not already installed):
   ```bash
   sudo apt-get install mysql-server
   ```

2. **Create Database and User**:
   ```sql
   CREATE DATABASE inventory_db;
   CREATE USER 'inventory_user'@'localhost' IDENTIFIED BY 'password';
   GRANT ALL PRIVILEGES ON inventory_db.* TO 'inventory_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

#### 3. **Create Models**

In `models.py`:

```python
from flask import Flask
from flask_mysql import MySQL

app = Flask(__name__)
app.config.from_object('config')

mysql = MySQL()
mysql.init_app(app)

class Product:
    def __init__(self, id, name, quantity, price):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price

    @staticmethod
    def get_all():
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        cursor.close()
        conn.close()
        return products

    @staticmethod
    def get_by_id(product_id):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = cursor.fetchone()
        cursor.close()
        conn.close()
        return product

    @staticmethod
    def add(name, quantity, price):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, quantity, price) VALUES (%s, %s, %s)", (name, quantity, price))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update(product_id, name, quantity, price):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET name=%s, quantity=%s, price=%s WHERE id=%s", (name, quantity, price, product_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete(product_id):
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
        conn.commit()
        cursor.close()
        conn.close()
```

#### 4. **Create Forms**

In `forms.py`:

```python
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
```

#### 5. **Create Views**

In `app.py`:

```python
from flask import Flask, render_template, redirect, url_for, request
from forms import ProductForm
from models import Product

app = Flask(__name__)
app.config.from_object('config')

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
```

#### 6. **Configure Flask App**

In `config.py`:

```python
import os

SECRET_KEY = os.urandom(24)
MYSQL_DATABASE_USER = 'inventory_user'
MYSQL_DATABASE_PASSWORD = 'password'
MYSQL_DATABASE_DB = 'inventory_db'
MYSQL_DATABASE_HOST = 'localhost'
```

#### 7. **Create Templates**

Create templates in `templates/`.

**base.html**:

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

**products.html**:

```html
{% extends 'base.html' %}

{% block title %}Products{% endblock %}

{% block content %}
<h2>Product List</h2>
<a href="{{ url_for('add_product') }}">Add Product</a>
<table>
    <thead>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Quantity</th>
            <th>Price</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for product in products %}
        <tr>
            <td>{{ product[0] }}</td>
            <td>{{ product[1] }}</td>
            <td>{{ product[2] }}</td>
            <td>{{ product[3] }}</td>
            <td>
                <a href="{{ url_for('edit_product', product_id=product[0]) }}">Edit</a>
                <a href="{{ url_for('delete_product', product_id=product[0]) }}">Delete</a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

**add_product.html**:

```html
{% extends 'base.html' %}

{% block title %}Add Product{% endblock %}

{% block content %}
<h2>Add Product</h2>
<form method="POST">
    {{ form.hidden_tag() }}
    <div>
        {{ form.name.label }}<br>
        {{ form.name(size=32) }}
    </div>
    <div>
        {{ form.quantity.label }}<br>
        {{ form.quantity() }}
    </div>
    <div>
        {{ form.price.label }}<br>
        {{ form.price() }}
    </div>
    <button type="submit">Add Product</button>
</form>
<a href="{{ url_for('index') }}">Back to Product List</a>
{% endblock %}
```

**edit_product.html**:

```html
{% extends 'base.html' %}

{% block title %}Edit Product{% endblock %}

{% block content %}
<h2>Edit Product</h2>
<form method="POST">
    {{ form.hidden_tag() }}
    <div>
        {{ form.name.label }}<br>
        {{ form.name(size=32) }}
    </div>
    <div>
        {{ form.quantity.label }}<br>
        {{ form.quantity() }}
    </div>
    <div>
        {{ form.price.label }}<br>
        {{ form.price() }}
    </div>
    <button type="submit">Update Product</button>
</form>
<a href="{{ url_for('index') }}">Back to Product List</a>
{% endblock %}
```

#### 8. **Add Static Files and Basic Styling**

Create a CSS file for basic styling.

**static/styles.css**:

```css
body {
    font-family: Arial, sans-serif;
    background-color: #f2f2f2;
    margin: 0;
    padding: 0;
}

.container {
    width: 80%;
    margin: auto;
    overflow: hidden;
}

h2 {
    color: #333;
}

form {
    margin: 20px;
    padding: 20px;
    background: #fff;
    border: 1px solid #ddd;
}

table {
    width: 100%;
    border-collapse: collapse;
}

table, th, td {
    border: 1px solid #ddd;
}

th, td {
    padding: 8px;
    text-align: left;
}

a {
    display: block;
    margin: 20px 0;
    text-decoration: none;
```css
}

a:hover {
    text-decoration: underline;
}

button {
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}
```

### SQL for Tables

```sql
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Overview of the Project

#### Project Description
The Inventory Management System allows users to manage an inventory of products. Users can add new products, update existing products, delete products, and view a list of all products in the inventory.

#### Features
1. **Product Management**: Add, update, and delete products.
2. **Product Listing**: View a list of all products.
3. **Product Details**: View detailed information about each product.

### How to Set Up and Connect Database

#### Prerequisites
- Python and pip installed.
- Flask and MySQL client installed.

#### Steps

1. **Set Up the Flask Project**:
   - Install necessary packages: `pip install flask flask-mysql flask-wtf`.
   - Create the project directory structure.

2. **Configure the MySQL Database**:
   - Install MySQL server if not already installed: `sudo apt-get install mysql-server`.
   - Create the database and user:
     ```sql
     CREATE DATABASE inventory_db;
     CREATE USER 'inventory_user'@'localhost' IDENTIFIED BY 'password';
     GRANT ALL PRIVILEGES ON inventory_db.* TO 'inventory_user'@'localhost';
     FLUSH PRIVILEGES;
     ```

3. **Define Models**:
   - Implement the `Product` class in `models.py` for handling product data and database operations.

4. **Create Forms**:
   - Define the `ProductForm` class in `forms.py` for product input forms.

5. **Implement Views**:
   - Create view functions in `app.py` for listing products, adding new products, editing products, and deleting products.

6. **Configure Flask Application**:
   - Set the database connection and secret key in `config.py`.

7. **Create HTML Templates**:
   - Develop templates for product listing (`products.html`), adding products (`add_product.html`), and editing products (`edit_product.html`).

8. **Add Static Files and Styling**:
   - Create `styles.css` in the `static` directory for basic styling.

9. **Run Migrations**:
   - Ensure the `products` table is created in the MySQL database.

10. **Run the Flask Application**:
    ```bash
    python app.py
    ```

11. **Access the Application**:
    - Open a web browser and go to `http://127.0.0.1:5000/` to view the product list and manage the inventory.

### Result

The Inventory Management System should now be functional. Users can add, update, and delete products, and view a list of all products in the inventory. Here are some sample results:

1. **Product List**:
   ```
   ID | Name         | Quantity | Price  | Actions
   ---|--------------|----------|--------|--------------------
   1  | Product A    | 10       | 100.00 | Edit | Delete
   2  | Product B    | 5        | 50.00  | Edit | Delete
   ```

2. **Add Product Form**:
   ```
   Name: [____________]
   Quantity: [____]
   Price: [______]
   [Add Product Button]
   ```

3. **Edit Product Form**:
   ```
   Name: [____________]
   Quantity: [____]
   Price: [______]
   [Update Product Button]
   ```

### Conclusion

By following the outlined procedure, you have developed a functional Inventory Management System using Flask and MySQL. The application includes features for managing product inventory, including adding, updating, and deleting products, and viewing product details. This project demonstrates a practical application of web development and database management concepts.