from mysql.connector import pooling
def create_db():
    # Connect to database and create connection pool
    mydb = pooling.MySQLConnectionPool(
        host="localhost",
        user="root",
        password="password",
        database="website",
        pool_name="mypool",
        pool_size=5
    )

    return mydb