from flask import Blueprint, request
import requests
import time
from model.tappay import partner_key
from flask import session
import jwt
from routes.auth import jwt_secret
from model.model import mydb

order_bp = Blueprint("order", __name__)

@order_bp.route("/api/orders", methods=["POST"])
# Get payment data and send to TapPay
def submit_order():
    # Verify if the jwt exists and is decodable from the token
    try:
        assert "token" in session
        token = session["token"]
        decode_token = jwt.decode(token, jwt_secret, algorithms="HS256")
        user_id = decode_token["id"]
    except: # Token invalid => denied access
        error = "未登入系統，拒絕存取"
        res = {
            "error": True,
            "message": error
        }
        return res, 403
    # Run pre-payment process and store payment data into database
    try:
        # Get payment data from front-end request
        order_prime = request.json["prime"]
        order_price = request.json["order"]["price"]
        order_attraction_id = request.json["order"]["trip"]["attraction"]["id"]
        order_attraction_name = request.json["order"]["trip"]["attraction"]["name"]
        # order_attraction_address = request.json["order"]["trip"]["attraction"]["address"]
        # order_attraction_image = request.json["order"]["trip"]["attraction"]["image"]
        order_date = request.json["order"]["trip"]["date"]
        order_time = request.json["order"]["trip"]["time"]
        order_contact_name = request.json["order"]["contact"]["name"]
        order_contact_email = request.json["order"]["contact"]["email"]
        order_contact_phone = request.json["order"]["contact"]["phone"]
        # Order number rule is 
        # YYYYMMDDHHMMSS + the milliseconds between the seconds (to the seventh digit after the decimal point)
        # e.g. YYYYMMDDHHMMSS1234567
        # e.g. 202212250800201234567
        order_number = time.strftime(
            "%Y%m%d%H%M%S") + str(time.time()).replace(".", "")[-7:]
        # Get the amount based on ordered trip time
        order_status = "unpaid"
        if order_time == "morning":
            amount = 2000
        if order_time == "afternoon":
            amount = 2500
        # Connect and insert the payment data into database 
        connection_object = mydb.get_connection()
        if connection_object.is_connected():
            website_cursor = connection_object.cursor()
            sql = '''
            INSERT INTO `order` ( \
                `order_number`, \
                `user_id`, \
                `date`, \
                `time`, \
                `attraction_id`, \
                `amount`, \
                `name`, \
                `email`, \
                `phone_number`, \
                `order_status`
                ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                '''
            val = (order_number, user_id, order_date, order_time, order_attraction_id, amount, order_contact_name, order_contact_email, order_contact_phone, order_status)
            website_cursor.execute(sql, val)
            connection_object.commit()
    # Error occurs during process
    except:
        error = "訂單建立失敗，輸入不正確或其他原因"
        res = {
            "error": True,
            "message": error
        }
        return res, 400
    # Run payment process and store result into database
    # Send payment request to TapPay API
    try:
        tap_pay_url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"  # Test environment
        header = {
            "Content-Type": "application/json",
            "x-api-key": partner_key
        }
        order = {
            "prime": order_prime,
            "partner_key": partner_key,
            "merchant_id": "bozemendless_CTBC",
            "amount": amount,
            "order_number": order_number,
            "details": order_attraction_name,
            "cardholder": {
                "phone_number": order_contact_phone,
                "name": order_contact_name,
                "email": order_contact_email
            }
        }
        # Get response from TapPay server
        response = requests.post(tap_pay_url, json=order, headers=header)
        resp = response.json()
        # Status code == 0 ==> success
        if resp["status"] == 0:
            sql = '''
            UPDATE `order` SET \
                `status_code` = %s, \
                `msg` = %s, \
                `rec_trade_id` = %s, \
                `bank_transaction_id` = %s, \
                `auth_code` = %s \
                WHERE `order_number` = %s
                '''
            val = (resp["status"], resp["msg"], resp["rec_trade_id"], resp["bank_transaction_id"], resp["auth_code"], order_number)
            website_cursor.execute(sql, val)
            connection_object.commit()
            sql = "UPDATE `order` SET `order_status` = 'paid' WHERE `order_number` = %s"
            val = (order_number,)
            website_cursor.execute(sql, val)
            connection_object.commit()
            website_cursor.close()
            res = {
                "data": {
                    "number": order_number,
                    "payment": {
                        "status": 0,
                        "message": "付款成功"
                    }
                }
            }
            return res
        # Status code !== 0 ==> something goes wrong
        else:
            # Store payment result from response into database
            sql = '''
            UPDATE `order` SET \
                `status_code` = %s, \
                `msg` = %s \
                WHERE `order_number` = %s
                '''
            val = (resp["status"], resp["msg"], order_number)
            website_cursor.execute(sql, val)
            connection_object.commit()
            connection_object.close()
            res = {
                "data": {
                    "number": order_number,
                    "payment": {
                        "status": resp["status"],
                        "message": "付款失敗"
                    }
                }
            }
            return res

    except:
        error = "伺服器內部錯誤"
        res = {
            "error": True,
            "message": error
        }
        return res, 500

@order_bp.route("/api/order/<order_number>")
# Get trip and order information from database
def get_order_data(order_number):
    # Verify if the jwt exists and is decodable from the token
    try:
        assert "token" in session
        token = session["token"]
        decode_token = jwt.decode(token, jwt_secret, algorithms="HS256")
        # user_id = decode_token["id"]
    except:
        error = "未登入系統，拒絕存取"  # Token invalid => denied access
        res = {
            "error": True,
            "message": error
        }
        return res, 403
    try:
        # Get trip and order information from database
        connection_object = mydb.get_connection()
        if connection_object.is_connected():
            website_cursor = connection_object.cursor()
            sql = '''
            SELECT \
                `order`.`amount`, \
                `attractions`.`id`, \
                `attractions`.`name`, \
                `attractions`.`address`, \
                `attractions`.`images`, \
                `order`.`date`, \
                `order`.`time`, \
                `order`.`name`, \
                `order`.`email`, \
                `order`.`phone_number`, \
                `order`.`status_code` \
            FROM `order` \
            INNER JOIN `attractions` ON \
                `order`.`attraction_id` = `attractions`.`id` \
            WHERE `order`.`order_number` = %s
            '''
            val = (order_number,)
            website_cursor.execute(sql, val)
            order_result = website_cursor.fetchone()
            connection_object.close()

            # Order_number not exist
            if order_result == None:
                res = {
                    "data": None
                }
                return res
        res = {
            "data": {
                "number": order_number,
                "price": order_result[0],
                "trip": {
                    "attraction": {
                        "id": order_result[1],
                        "name": order_result[2],
                        "address": order_result[3],
                        "image": "https://" + order_result[4].split("https://")[1]
                    },
                    "date": str(order_result[5]),
                    "time": order_result[6]
                },
                "contact": {
                    "name": order_result[7],
                    "email": order_result[8],
                    "phone": order_result[9]
                },
                "status": order_result[10]
            }
        }
        return res
    except:
        error = "伺服器內部錯誤"
        res = {
            "error": True,
            "message": error
        }
        return res, 500