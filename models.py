from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer,primary_key=True)
    isbn = db.Column(db.String,nullable=False)
    title = db.Column(db.String,nullable=False)
    author = db.Column(db.String,nullable=False)
    year = db.Column(db.String,nullable=False)

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer,primary_key=True)
    isbn = db.Column(db.String,nullable=False)
    review_user = db.Column(db.String,nullable=False)
    rating = db.Column(db.Integer,nullable=False)
    review = db.Column(db.String,nullable=False)
