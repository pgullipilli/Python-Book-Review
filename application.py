import os

from flask import Flask, session,render_template,request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success",methods=["POST"])
def success():
    username = request.form.get("username")
    username = username.capitalize()
    button = request.form.get("login")
    print(button)
    if button=="LOGIN":
        message = username + " you are logged in succcusfully!"
    else:
        message = username + " you are registered succcusfully!"
    return render_template('success.html',message=message)

# def login():
#     username = request.form.get("username")
#     username = username.capitalize()
#     message = username + " you are logged in succcusfully!"
#     return render_template('sucusses.html',message=message)

@app.route("/register")
def register():
    # username = request.form.get("username")
    # username = username.capitalize()
    # message = username + " you are registered succcusfully!"
    return render_template('register.html')
