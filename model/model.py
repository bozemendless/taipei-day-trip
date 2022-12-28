from mysql.connector import pooling

import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

# Connect to database and create connection pool
mydb = pooling.MySQLConnectionPool(
    host=host,
    user=user,
    password=password,
    database=database,
    pool_name="my_pool",
    pool_size=5
)