import os
import requests
import json

from flask import Flask, session, render_template, request,jsonify,json
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import urandom

from models import *

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

secret_key = config['GOODREADS']['API_KEY']


app = Flask(__name__)

# count = 1

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

app.secret_key = urandom(24)


Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    if 'username' in session:
        message = session['username'] + " you are currently logged in!!!"
        return render_template('success.html', message=message)
    return render_template("index.html")


@app.route("/success", methods=["POST"])
def success():
    global count
    username = request.form.get("username")
    form_password = request.form.get("password")
    button = request.form.get("login")

    if button == "LOGIN":
        user = db.execute("select * from users where name=:username",
                          {"username": username}).fetchone()

        if user == ' ' or user.password != form_password:
            message = "check username or password"

        elif user.password == form_password:
            # print(user.password)
            session['username'] = username
            session['username'] = session['username'].capitalize()
            message = session['username'] + " you are logged in succcusfully!"

    else:
        count_value = db.execute("select count(*) from users").fetchone()
        count = count_value[0]
        count = int(count)+1
        # print(count)
        db.execute("INSERT INTO users (id,name, password) VALUES (:id,:name, :password)", {
                   "id": count, "name": username, "password": form_password})
        db.commit()
        # count += 1
        session['username'] = username
        session['username'] = session['username'].capitalize()
        message = session['username'] + " you are registered succcusfully!"
    return render_template('success.html', message=message)


@app.route("/register")
def register():
    return render_template('register.html')


@app.route('/sign_out')
def sign_out():
    session.pop('username')
    return render_template("index.html")


@app.route('/search', methods=["POST"])
def search():
    isbn = request.form.get('isbn')
    title = request.form.get('title')
    author = request.form.get('author')

    filtered_list = []

    if isbn != '' or title != '' or author != '':
        books = db.execute('select * from books').fetchall()
    else:
        books = None

    count_value = db.execute("select count(*) from books").fetchone()
    count = count_value[0]
    count = int(count)+1
    counter = 1

    if books != None:
        for i in books:
            if isbn == '' and title == '' and author == '':
                # print('No Such Book')
                break
            elif isbn != '' and title == '' and author == '':
                if i.isbn.find(isbn) != -1:
                    filtered_list.append(i)
                    # print(i)
                else:
                    counter += 1
                    if counter == count:
                        # print('No Such Book')
                        break

            elif isbn == '' and title != '' and author == '':
                if title in i.title.lower() != -1:
                    filtered_list.append(i)
                    # print(i)
                else:
                    counter += 1
                    if counter == count:
                        # print('No Such Book')
                        break

            elif isbn == '' and title == '' and author != '':
                if author in i.author.lower() != -1:
                    filtered_list.append(i)
                    # print(i)
                else:
                    counter += 1
                    if counter == count:
                        # print('No Such Book')
                        break

            elif isbn != '' and title != '' and author == '':
                if i.isbn.find(isbn) != -1 and title in i.title.lower() != -1:
                    filtered_list.append(i)
                    # print(i)
                else:
                    counter += 1
                    if counter == count:
                        # print('No Such Book')
                        break

            elif isbn != '' and title == '' and author != '':
                if i.isbn.find(isbn) != -1 and author in i.author.lower() != -1:
                    filtered_list.append(i)
                    # print(i)
                else:
                    counter += 1
                    if counter == count:
                        # print('No Such Book')
                        break

            elif isbn == '' and title != '' and author != '':
                if title in i.title.lower() != -1 and author in i.author.lower() != -1:
                    filtered_list.append(i)
                    # print(i)
                else:
                    counter += 1
                    if counter == count:
                        # print('No Such Book')
                        break

            else:
                # print('No Such Book')
                break
        books = filtered_list
    return render_template('search.html', books=books)


@app.route('/review/<string:isbn>')
def review(isbn):
    review_user = session['username']
    book = db.execute('select * from books where isbn=:isbn',
                      {"isbn": isbn}).fetchone()
    exist_review = db.execute('select * from reviews where isbn=:isbn AND review_user=:review_user', {
                              "isbn": isbn, "review_user": review_user}).fetchone()
    # isbn = book.isbn
    # title = book.title
    # author = book.author
    # year = book.year

    res = requests.get("https://www.goodreads.com/book/review_counts.json",params={"key":secret_key,"isbns": book.isbn})
    result = res.json()
    good_reads_rating_count = result["books"][0]["work_ratings_count"]
    good_reads_avg_rating = result["books"][0]["average_rating"]

    return render_template('result.html',book=book,exist_review=exist_review,good_reads_avg_rating = good_reads_avg_rating,good_reads_rating_count = good_reads_rating_count)


@app.route('/review_feedback', methods=['POST'])
def review_feedback():
    isbn = request.form.get('isbn')
    title = request.form.get('title')
    review_user = session['username']
    exist_review = db.execute('select * from reviews where isbn=:isbn AND review_user=:review_user', {
                              "isbn": isbn, "review_user": review_user}).fetchone()
    if exist_review == None:
        rating = request.form.get('rating')
        rating_int = int(rating)
        review = request.form.get('review')
        # review_user = user.lower()
        # print(exist_review)

        count_value = db.execute("select count(*) from reviews").fetchone()
        count = count_value[0]
        count = int(count)+1
        # counter = 1


        db.execute("INSERT INTO reviews (id,isbn,review_user,rating,review) VALUES (:id,:isbn,:review_user,:rating,:review)", {
                   "id": count, "isbn": isbn, "review_user": review_user, "rating": rating_int, "review": review})
        db.commit()
        message = "Your Review submitted succusfully!"
        return render_template('feedback.html', message=message,exist_review=exist_review)
    else:
        message = "Your review for this book is"
        return render_template('feedback.html', message=message,exist_review=exist_review,title=title,isbn=isbn)


@app.route('/api/<string:isbn>')
def books_api(isbn):
    book = db.execute('select * from books where isbn=:isbn',
                      {"isbn": isbn}).fetchone()
    if book == None:
        return jsonify({"error":"Book Not Found"}),404
        # return abort(404)
    else:
        res = requests.get("https://www.goodreads.com/book/review_counts.json",params={"key":secret_key,"isbns": book.isbn})
        result = res.json()
        good_reads_rating_count = result["books"][0]["work_ratings_count"]
        good_reads_avg_rating = result["books"][0]["average_rating"]
        return jsonify({
            "title":book.title,
            "author":book.author,
            "year":book.year,
            "isbn":book.isbn,
            "review_count":good_reads_rating_count,
            "average_score":good_reads_avg_rating
        })
