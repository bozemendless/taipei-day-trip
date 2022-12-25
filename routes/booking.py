from flask import request, Blueprint, session
from model.model import mydb
import jwt
from routes.auth import jwt_secret

booking_bp = Blueprint("booking", __name__)


@booking_bp.route("/api/booking", methods=["GET", "POST", "DELETE"])
def attractionBooking():
    # GET method # Get the booked data
    if request.method == "GET":
        if "token" in session: # If token exists
            connection_object = mydb.get_connection()
            if connection_object.is_connected():
                website_cursor = connection_object.cursor()
                try:
                    token = session["token"]
                    decode_token = jwt.decode(token, jwt_secret, algorithms="HS256")
                except: # Token invalid
                    error = "無效的憑證"
                    res = {
                        "error": True,
                        "message": error
                    }
                    return res, 401
                id = int(decode_token["id"])
                sql = "SELECT \
                `attractions`.`id`, \
                `attractions`.`name`, \
                `attractions`.`address`, \
                `attractions`.`images`, \
                `booking`.`date`, \
                `booking`.`time` \
                FROM `booking` \
                INNER JOIN `attractions` ON `booking`.`attraction_id` = `attractions`.`id` \
                WHERE `booking`.`user_id` = %s"
                val = (id,)
                website_cursor.execute(sql, val)
                bookingResult = website_cursor.fetchone()
                website_cursor.close()
                connection_object.close()
                if bookingResult == None: # Booking data not exist
                    res = {
                        "data":None
                    }
                    return res

                # Deal with booking data
                if bookingResult[5] == "morning":
                    price = 2000
                if bookingResult[5] == "afternoon":
                    price = 2500
                res = {
                    "data": {
                        "attractions": {
                            "id": bookingResult[0],
                            "name": bookingResult[1],
                            "address": bookingResult[2],
                            "image": "https://" + bookingResult[3].split("https://")[1]
                        },
                        "date": str(bookingResult[4]),
                        "time": bookingResult[5],
                        "price": price
                    }
                }
                return res
        if "token" not in session: # If token not exist
            error = "未登入系統，拒絕存取"
            res = {
                "error": True,
                "message": error
            }
            return res, 403

    # POST method # Create a new booking
    if request.method == "POST":
        try:
            # Insert new booking data into database 
            if "token" in session:
                try:
                    attraction_id = request.json["attractionId"]
                    date = request.json["date"]
                    time = request.json["time"]
                    price = request.json["price"]
                    try: # Check if token is valid
                        token = session["token"]
                        decode_token = jwt.decode(
                            token, jwt_secret, algorithms="HS256")
                        user_id = decode_token["id"]
                    except: # Token invalid
                        error = "無效的憑證"
                        res = {
                            "error": True,
                            "message": error
                        }
                        return res, 401
                    connection_object = mydb.get_connection() # Connect to pool
                    if connection_object.is_connected():
                        website_cursor = connection_object.cursor()
                        sql = "SELECT `user_id` FROM `booking` WHERE `user_id` = %s"
                        val = (user_id,)
                        website_cursor.execute(sql, val)
                        exist_result = website_cursor.fetchone()
                        if exist_result != None: # Check if booking data exists, if so, delete previous data
                            sql = "DELETE FROM `booking` WHERE `user_id` = %s"
                            val = (user_id,)
                            website_cursor.execute(sql, val)
                            connection_object.commit()
                        sql = "INSERT INTO `booking` (`user_id`, `attraction_id`, `date`, `time`) VALUES (%s, %s, %s, %s)" # Insert booking data into the table
                        val = (user_id, attraction_id, date, time)
                        website_cursor.execute(sql, val)
                        connection_object.commit()
                        connection_object.close()
                        return {"ok": True}
                except:
                    error = "建立失敗，輸入不正確或其他原因" # Fail or errors occur during inserting the booking data into
                    res = {
                        "error": True,
                        "message": error
                    }
                    return res, 400
            if "token" not in session:
                error = "未登入系統，拒絕存取"
                res = {
                    "error": True,
                    "message": error
                }
                return res, 403
        except:
            error = "伺服器內部錯誤"
            res = {
                "error":True,
                "message": error
            }
            return res, 500

    # DELETE method # Delete the current booking
    if request.method == "DELETE":
        try:
            # Check if the booking data already exists
            connection_object = mydb.get_connection()
            if connection_object.is_connected(): 
                website_cursor = connection_object.cursor()
                try: # Check if token is valid
                    token = session["token"]
                    decode_token = jwt.decode(
                        token, jwt_secret, algorithms="HS256")
                    user_id = decode_token["id"]
                except:
                    # Token invalid
                    error = "無效的憑證"
                    res = {
                        "error": True,
                        "message": error
                    }
                    return res, 401
                sql = "SELECT `user_id` FROM `booking` WHERE `user_id` = %s" # Get the booking data
                val = (user_id,)
                website_cursor.execute(sql,val)
                exist_result = website_cursor.fetchone()
                if exist_result != None: # Check if the booking data exists
                    sql = "DELETE FROM `booking` WHERE `user_id` = %s"
                    val = (user_id,)
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
