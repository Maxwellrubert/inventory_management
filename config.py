import os

SECRET_KEY = os.urandom(24)
MYSQL_DATABASE_USER = 'inventory_user'
MYSQL_DATABASE_PASSWORD = 'password'
MYSQL_DATABASE_DB = 'inventory_db'
MYSQL_DATABASE_HOST = 'localhost'  # Add this line if it's missing