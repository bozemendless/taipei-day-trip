from flask import request, session, Blueprint
import jwt
import datetime
from datetime import timedelta
from model.model import create_db

mydb = create_db

jwt_secret = "446EAFA08BC9FC19DFBF92E1ACD11B3355CF9626FA6EAA03646FD2EBD588E9F4"

auth = Blueprint("auth", __name__)

@auth.route("/api/user", methods=["POST"])
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


@auth.route("/api/user/auth", methods=["GET", "PUT", "DELETE"])
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
                    decodeToken = jwt.decode(
                        token, jwt_secret, algorithms="HS256")
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
                loginResult = websiteCursor.fetchone()  # (id, name) or None
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
