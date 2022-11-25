from flask import *
from mysql.connector import pooling
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"]=False

# Set the session key
app.secret_key = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf' # this is the example on documentation

# Connect to database and create connection pool
mydb = pooling.MySQLConnectionPool(
    host="localhost",
    user="root",
    password="password",
    database="website",
    pool_name="mypool",
    pool_size=5
)

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

# APIs
@app.route("/api/attractions")
def attractions():
    try:
        # # Check if session exists
        # if 'username' not in session:
        #     return redirect('/')

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
                data.append({"id":attraction[0],
                        "name":attraction[1],
                        "category":attraction[2],
                        "description":attraction[3],
                        "address":attraction[4],
                        "transport": attraction[5],
                        "mrt":attraction[6],
                        "lat":float(attraction[7]),
                        "lng": float(attraction[8]),
                        "images": ["https://" + link for link in attraction[9].split("https://") if link != ""]
                    })

            res = {
                "nextPage": nextPage,
                "data":data
            }

            response = make_response(res)
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response

    # Error handler 500
    except:
        error = "伺服器內部錯誤"
        res = {
                "error": True,
                "message": error
            }
        return res, 500

@app.route("/api/attraction/<id>")
def attractionId(id):
    try:
        # Connect to connection pool
        connectionObject = mydb.get_connection()

        if connectionObject.is_connected():

            # Get data from database
            websiteCursor = connectionObject.cursor()

            sql = "SELECT * FROM `attractions` WHERE id = %s"
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

            data = {"id":attractionsResult[0],
                        "name":attractionsResult[1],
                        "category":attractionsResult[2],
                        "description":attractionsResult[3],
                        "address":attractionsResult[4],
                        "transport": attractionsResult[5],
                        "mrt":attractionsResult[6],
                        "lat":float(attractionsResult[7]),
                        "lng": float(attractionsResult[8]),
                        "images": ["https://" + link for link in attractionsResult[9].split("https://") if link != ""]
                    }
            
            res = {
                "data":data
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

@app.route("/api/categories")
def categories():

    try:
        # Connect to connection pool
        connectionObject = mydb.get_connection()

        if connectionObject.is_connected():

            # Get data from database
            websiteCursor = connectionObject.cursor()

            sql = "SELECT DISTINCT category FROM attractions;"

            websiteCursor.execute(sql)

            categoriesResult = websiteCursor.fetchall()

            connectionObject.close()

            # Deal with the response from database then return the response
            categories = [category[0] for category in categoriesResult]

        res = {
            "data":categories
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

app.run(host="0.0.0.0", port=3000)