import csv
import os

from flask import Flask, render_template, request
from models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

count_value = db.execute("select count(*) from books").fetchone()
count = count_value[0]
count = int(count)+1

def main():
    global count
    f = open("books.csv")
    reader = csv.reader(f)
    next(reader, None)
    for isbn, title, author, year in reader:

        db.execute("INSERT INTO books (id,isbn,title,author,year) VALUES (:id,:isbn,:title,:author,:year)",{"id":count,"isbn": isbn, "title": title, "author":author,"year":year})
        db.commit()
        count += 1

if __name__ == "__main__":
    with app.app_context():
        main()