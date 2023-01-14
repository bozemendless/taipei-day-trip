from routes.booking import booking_bp
from routes.auth import auth
from routes.attraction import attraction_bp
from routes.order import order_bp
from flask import Flask, render_template
import os
from dotenv import load_dotenv

load_dotenv()

secret_key = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["JSON_SORT_KEYS"] = False
app.config["SECRET_KEY"] = secret_key

app.register_blueprint(attraction_bp)
app.register_blueprint(auth)
app.register_blueprint(booking_bp)
app.register_blueprint(order_bp)

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


# @app.route("/member")
# def member():
#     return render_template("member.html")


app.run(host="0.0.0.0", port=80, debug=False)