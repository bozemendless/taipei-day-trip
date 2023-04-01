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

def get_attractions(page, keyword):
    # Get connection from connection pool
    with mydb.get_connection() as connection_object:
        if connection_object.is_connected():

            # Get data from database
            website_cursor = connection_object.cursor()

            if keyword == None:
                # Get total count of rows
                sql_count = "SELECT COUNT(id) FROM `attractions`"
                website_cursor.execute(sql_count)
                number_of_row = website_cursor.fetchone()[0]

                # Get attractions results
                sql = "SELECT * FROM `attractions`"
                limit = f" LIMIT {(page) * 12},12"
                sql += limit
                website_cursor.execute(sql)
                attractions_result = website_cursor.fetchall()

            else:
                # Get total count of rows
                sql_count = "SELECT COUNT(id) FROM `attractions` WHERE `category` = %s or `name` LIKE %s"
                val = keyword, "%"+keyword+"%"
                website_cursor.execute(sql_count, val)
                number_of_row = website_cursor.fetchone()[0]

                # Get attractions results
                sql = "SELECT * FROM `attractions` WHERE `category` = %s or `name` LIKE %s"
                limit = f" LIMIT {(page) * 12},12"
                sql += limit
                website_cursor.execute(sql, val)
                attractions_result = website_cursor.fetchall()

            # Deal with the response from database then return the response
            next_page = page + 1
            if number_of_row - (page + 1) * 12 <= 0:
                next_page = None

            data = []
            for attraction in attractions_result:
                data.append({"id": attraction[0],
                            "name": attraction[1],
                            "category": attraction[2],
                            "description": attraction[3],
                            "address": attraction[4],
                            "transport": attraction[5],
                            "mrt": attraction[6],
                            "lat": float(attraction[7]),
                            "lng": float(attraction[8]),
                            "images": ["https://" + link for link in attraction[9].split("https://") if link != ""]
                            })

            res = {
                "nextPage": next_page,
                "data": data
            }

            return res

def get_attraction_by_id(id):
    # Get connection from connection pool
    with mydb.get_connection() as connection_object:
        if connection_object.is_connected():
            # Get data from database
            website_cursor = connection_object.cursor()

            sql = "SELECT * FROM `attractions` WHERE `id` = %s"
            val = (id,)

            website_cursor.execute(sql, val)

            attractions_result = website_cursor.fetchone()

            # Deal with the response from database then return the response
            # Error handler 400
            if attractions_result == []:
                error = "景點編號不正確"
                res = {
                    "error": True,
                    "message": error
                }
                return res, 400

            data = {"id": attractions_result[0],
                    "name": attractions_result[1],
                    "category": attractions_result[2],
                    "description": attractions_result[3],
                    "address": attractions_result[4],
                    "transport": attractions_result[5],
                    "mrt": attractions_result[6],
                    "lat": float(attractions_result[7]),
                    "lng": float(attractions_result[8]),
                    "images": ["https://" + link for link in attractions_result[9].split("https://") if link != ""]
                    }

            res = {
                "data": data
            }
            return res
