from flask import *
from mysql.connector import pooling
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

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
        connection_object = mydb.get_connection()

        if connection_object.is_connected():

            # Get data from database
            website_cursor = connection_object.cursor()

            where = f" WHERE `category` = '{keyword}' or `name` LIKE '%{keyword}%'"
            limit = f" LIMIT {(page) * 12},12"

            sqlCount = "SELECT COUNT(id) FROM `attractions`"
            if keyword != None:
                sqlCount += where

            website_cursor.execute(sqlCount)
            numberOfRow = website_cursor.fetchone()[0]

            sql = "SELECT * FROM `attractions`"
            if keyword != None:
                sql += where
            if page != None:
                sql += limit

            website_cursor.execute(sql)

            user_name_result = website_cursor.fetchall()

            connection_object.close()
            
            # Deal with the response from database then return the response
            nextPage = page + 1
            if numberOfRow - (page + 1) * 12 <= 0:
                nextPage = None

            data = []
            for attraction in user_name_result:
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

            return res
    except:
        error = "伺服器內部錯誤"
        res = {
                "error": True,
                "message": error
            }
        return res

app.run(port=3000, debug=True)