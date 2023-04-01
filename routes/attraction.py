from flask import Blueprint, request, redirect
from model.model import *

attraction_bp = Blueprint("attraction", __name__)

@attraction_bp.route("/api/attractions")
def get_all_attractions():
    try:
        # Receive data through get method
        try:
            page = int(request.args.get("page"))
            keyword = request.args.get("keyword")
        except:
            return redirect('/')

        res = get_attractions(page, keyword)
        return res

    # Error handler 500
    except:
        error = "伺服器內部錯誤"
        res = {
            "error": True,
            "message": error
        }
        return res, 500


@attraction_bp.route("/api/attraction/<id>")
def get_attraction(id):
    try:
        res = get_attraction_by_id(id)
        return res

    # Error handler 500
    except:
        error = "伺服器內部錯誤"
        res = {
            "error": True,
            "message": error
        }
        return res, 500


@attraction_bp.route("/api/categories")
def categories():

    try:
        # Connect to connection pool
        connection_object = mydb.get_connection()

        if connection_object.is_connected():

            # Get data from database
            website_cursor = connection_object.cursor()

            sql = "SELECT DISTINCT `category` FROM `attractions`;"

            website_cursor.execute(sql)

            categories_result = website_cursor.fetchall()

            # Deal with the response from database then return the response
            categories = [category[0] for category in categories_result]

        res = {
            "data": categories
        }

        return res

    # Error handler 500
    except:
        error = "伺服器內部錯誤"
        res = {
            "error": True,
            "message": error
        }
        return res, 500

    # Close cursor and connection
    finally:
        try:
            website_cursor.close()
            connection_object.close()
        except Exception as e:
            print(e)
