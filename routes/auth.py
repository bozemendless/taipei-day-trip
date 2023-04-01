from flask import request, session, Blueprint
import jwt
import datetime
from datetime import timedelta
from model.model import mydb

jwt_secret = "446EAFA08BC9FC19DFBF92E1ACD11B3355CF9626FA6EAA03646FD2EBD588E9F4"

auth = Blueprint("auth", __name__)

@auth.route("/api/user", methods=["POST"])
def signup():
    # Try to deal with user signup data
    try:
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
    except:
        error = "欄位格式錯誤"
        res = {
            "error": True,
            "message": error
        }
        return res, 400
    # Try to sign up
    try:
        # Connect to connection pool
        connection_object = mydb.get_connection()
        if connection_object.is_connected():
            website_cursor = connection_object.cursor()
            # Check if email exists
            sql = "SELECT `email` FROM `user` WHERE `email` = %s;"
            val = (email,)
            website_cursor.execute(sql, val)
            email_result = website_cursor.fetchone()
            # If exists
            if email_result != None:
                error = "重複的 email "
                res = {
                    "error": True,
                    "message": error
                }
                return res, 400
            # Not exist >> sign up a new account to database
            sql = "INSERT INTO `user` (name, email, password) VALUES (%s, %s, SHA2(%s, 224))"
            val = (name, email, password)
            website_cursor.execute(sql, val)
            connection_object.commit()
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
    # Close cursor and connection
    finally:
        try:
            website_cursor.close()
            connection_object.close()
        except Exception as e:
            print(e)


@auth.route("/api/user/auth", methods=["GET", "PUT", "DELETE"])
def userAuth():
    # GET method # Get account information
    if request.method == "GET":
        try:
            # Check if logging status is valid
            if "token" in session:
                # Token valid
                try:
                    token = session["token"]
                    decode_token = jwt.decode(
                        token, jwt_secret, algorithms="HS256")
                    res = {
                        "data": {
                            "id": decode_token["id"],
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
                    return res, 401
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
        except:
            error = "帳號、密碼不得空白"
            res = {
                "error": True,
                "message": error
            }
            return res, 400
        # Check if the logging info corrects
        try:
            connection_object = mydb.get_connection()
            if connection_object.is_connected():
                website_cursor = connection_object.cursor()
                sql = "SELECT `id`, `name` FROM `user` WHERE `email` = %s and `password` = SHA2(%s, 224)"
                val = (email, password)
                website_cursor.execute(sql, val)
                login_result = website_cursor.fetchone()  # (id, name) or None
                # Not correct
                if login_result == None:
                    error = "帳號或密碼錯誤"
                    res = {
                        "error": True,
                        "message": error
                    }
                    return res, 400
                # Info corrects >> Make token by JWT-ing user's id
                payload = {
                    "id": login_result[0],
                    "exp": datetime.datetime.utcnow() + timedelta(days=7)
                }
                encoded_id = jwt.encode(payload, jwt_secret)
                # Set sessions
                session["token"] = encoded_id
                session["name"] = login_result[1]
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
        # Close cursor and connection
        finally:
            try:
                website_cursor.close()
                connection_object.close()
            except Exception as e:
                print(e)

    # DELETE method # Log out
    try:
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
