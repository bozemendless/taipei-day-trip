from flask import Blueprint, request, redirect
from model.model import mydb

attraction = Blueprint("attraction", __name__)

@attraction.route("/api/attractions")
def attractions():
    try:
        # Receive data through get method
        try:
            page = int(request.args.get("page"))
            keyword = request.args.get("keyword")
        except:
            return redirect('/')

        # Connect to connection pool
        connectionObject = mydb.get_connection()

        if connectionObject.is_connected():

            # Get data from database
            websiteCursor = connectionObject.cursor()

            if keyword == None:
                sqlCount = "SELECT COUNT(id) FROM `attractions`"
                websiteCursor.execute(sqlCount)
                numberOfRow = websiteCursor.fetchone()[0]

                sql = "SELECT * FROM `attractions`"
                limit = f" LIMIT {(page) * 12},12"
                sql += limit
                websiteCursor.execute(sql)
                attractionsResult = websiteCursor.fetchall()

            if keyword != None:
                sqlCount = "SELECT COUNT(id) FROM `attractions` WHERE `category` = %s or `name` LIKE %s"
                val = keyword, "%"+keyword+"%"
                websiteCursor.execute(sqlCount, val)
                numberOfRow = websiteCursor.fetchone()[0]

                sql = "SELECT * FROM `attractions` WHERE `category` = %s or `name` LIKE %s"
                limit = f" LIMIT {(page) * 12},12"
                sql += limit
                websiteCursor.execute(sql, val)
                attractionsResult = websiteCursor.fetchall()

            connectionObject.close()

            # Deal with the response from database then return the response
            nextPage = page + 1
            if numberOfRow - (page + 1) * 12 <= 0:
                nextPage = None

            data = []
            for attraction in attractionsResult:
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
                "nextPage": nextPage,
                "data": data
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


@attraction.route("/api/attraction/<id>")
def attractionId(id):
    try:
        # Connect to connection pool
        connectionObject = mydb.get_connection()

        if connectionObject.is_connected():

            # Get data from database
            websiteCursor = connectionObject.cursor()

            sql = "SELECT * FROM `attractions` WHERE `id` = %s"
            val = (id,)

            websiteCursor.execute(sql, val)

            attractionsResult = websiteCursor.fetchone()

            connectionObject.close()

            # Deal with the response from database then return the response
            # Error handler 400
            if attractionsResult == []:
                error = "景點編號不正確"
                res = {
                    "error": True,
                    "message": error
                }
                return res, 400

            data = {"id": attractionsResult[0],
                    "name": attractionsResult[1],
                    "category": attractionsResult[2],
                    "description": attractionsResult[3],
                    "address": attractionsResult[4],
                    "transport": attractionsResult[5],
                    "mrt": attractionsResult[6],
                    "lat": float(attractionsResult[7]),
                    "lng": float(attractionsResult[8]),
                    "images": ["https://" + link for link in attractionsResult[9].split("https://") if link != ""]
                    }

            res = {
                "data": data
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


@attraction.route("/api/categories")
def categories():

    try:
        # Connect to connection pool
        connectionObject = mydb.get_connection()

        if connectionObject.is_connected():

            # Get data from database
            websiteCursor = connectionObject.cursor()

            sql = "SELECT DISTINCT `category` FROM `attractions`;"

            websiteCursor.execute(sql)

            categoriesResult = websiteCursor.fetchall()

            connectionObject.close()

            # Deal with the response from database then return the response
            categories = [category[0] for category in categoriesResult]

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
