from flask import *
from mysql.connector import pooling
import jwt
import datetime
from datetime import timedelta
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSON_SORT_KEYS"]=False
app.config["SECRET_KEY"]="192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf"
jwt_secret = "446EAFA08BC9FC19DFBF92E1ACD11B3355CF9626FA6EAA03646FD2EBD588E9F4"

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

            # response = make_response(res)
            # response.headers.add("Access-Control-Allow-Origin", "*")
            # return response
            return res

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

            sql = "SELECT DISTINCT `category` FROM `attractions`;"

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

@app.route("/api/user", methods=["POST"])
def signup():
    try:
        assert "application/json" in request.headers["Accept"]
        # Check if column contains blank values
        name = request.json["name"]
        email = request.json["email"]
        password = request.json["password"]
        if name == "" or email == "" or password == "":
            error = "欄位格式錯誤"
            res = {
                "error": True,
                "message": error
            }
            return res, 400
        # Connect to connection pool
        connectionObject = mydb.get_connection()
        if connectionObject.is_connected():
            websiteCursor = connectionObject.cursor()
            # Check if email exists
            sql = "SELECT `email` FROM `user` WHERE `email` = %s;"
            val = (email,)
            websiteCursor.execute(sql, val)
            emailResult = websiteCursor.fetchone()
            # If exists
            if emailResult != None:
                connectionObject.close()
                error = "重複的 email "
                res = {
                    "error": True,
                    "message": error
                }
                return res, 400
            # Not exist >> sign up a new account to database
            sql = "INSERT INTO `user` (name, email, password) VALUES (%s, %s, SHA2(%s, 224))"
            val = (name, email, password)
            websiteCursor.execute(sql, val)
            connectionObject.commit()
            connectionObject.close()
            res = {
                "ok": True
            }
            return res
    except:
        error = "伺服器內部錯誤"
        res = {
            "error": True,
            "message": error
        }
        return res, 500

@app.route("/api/user/auth", methods=["GET", "PUT", "DELETE"])
def userAuth():
    # GET method # Get account information
    if request.method == "GET":
        try:
            assert "application/json" in request.headers["Accept"]
            # Check if logging status is valid
            if "token" in session:
                # Token valid
                try:
                    token = session["token"]
                    decodeToken = jwt.decode(token, jwt_secret, algorithms="HS256")
                    res = {
                        "data": {
                            "id": decodeToken["id"],
                            "name": session["name"],
                            "email": session["email"]
                        }
                    }
                    return res
                # Token invalid
                except:
                    error = "無效的憑證"
                    res = {
                        "error": True,
                        "message": error
                    }
                    return res
            # Not in logging status
            res = {
                "data": None
            }
            return res
        except:
            error = "伺服器內部錯誤"
            res = {
                "error": True,
                "message": error
            }
            return res, 500
    # PUT method # Log in
    if request.method == "PUT":
        try:
            assert "application/json" in request.headers["Accept"]
            email = request.json["email"]
            password = request.json["password"]
            # Check if column contains blank values
            if email == "" or password == "":
                error = "帳號、密碼不得空白"
                res = {
                    "error": True,
                    "message": error
                }
                return res, 400
            # Check if the logging info corrects
            connectionObject = mydb.get_connection()
            if connectionObject.is_connected():
                websiteCursor = connectionObject.cursor()
                sql = "SELECT `id`, `name` FROM `user` WHERE `email` = %s and `password` = SHA2(%s, 224)"
                val = (email, password)
                websiteCursor.execute(sql, val)
                loginResult = websiteCursor.fetchone() # (id, name) or None
                connectionObject.close()
                # Not correct
                if loginResult == None:
                    error = "帳號或密碼錯誤"
                    res = {
                        "error": True,
                        "message": error
                    }
                    return res, 400
                # Info corrects >> Make token by JWT-ing user's id
                payload = {
                    "id": loginResult[0],
                    "exp": datetime.datetime.utcnow() + timedelta(days=7)
                }
                encodedId = jwt.encode(payload, jwt_secret)
                # Set sessions
                session["token"] = encodedId
                session["name"] = loginResult[1]
                session["email"] = email
                res = {
                    "ok": True
                }
                return res
        except:
            error = "伺服器內部錯誤"
            res = {
                "error": True,
                "message": error
            }
            return res, 500
    # DELETE method # Log out
    try:
        assert "application/json" in request.headers["Accept"]
        if request.method == "DELETE":
            # Clear sessions
            for key in list(session.keys()):
                session.pop(key)
        res = {
            "ok": True
        }
        return res
    except:
        error = "伺服器內部錯誤"
        res = {
            "error": True,
            "message": error
        }
        return res, 500

app.run(host="0.0.0.0", port=3000)