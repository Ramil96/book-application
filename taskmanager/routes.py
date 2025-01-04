from flask import render_template
from taskmanager import app, db
from taskmanager.models import Genre, Book, Review


@app.route("/")
def home():
    # Pass genres and books to the template to display on the home page
    genres = Genre.query.all()
    books = Book.query.all()
    return render_template("base.html", genres=genres, books=books)
