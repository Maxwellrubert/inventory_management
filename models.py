class Product:
    mysql = None

    def __init__(self, id, name, quantity, price):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price

    @staticmethod
    def get_all():
        with Product.mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
        return products

    @staticmethod
    def get_by_id(product_id):
        with Product.mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products WHERE id=%s", (product_id,))
            product = cursor.fetchone()
        return product

    @staticmethod
    def add(name, quantity, price):
        with Product.mysql.connection.cursor() as cursor:
            cursor.execute("INSERT INTO products (name, quantity, price) VALUES (%s, %s, %s)", (name, quantity, price))
        Product.mysql.connection.commit()

    @staticmethod
    def update(product_id, name, quantity, price):
        with Product.mysql.connection.cursor() as cursor:
            cursor.execute("UPDATE products SET name=%s, quantity=%s, price=%s WHERE id=%s", (name, quantity, price, product_id))
        Product.mysql.connection.commit()

    @staticmethod
    def delete(product_id):
        with Product.mysql.connection.cursor() as cursor:
            cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
        Product.mysql.connection.commit()