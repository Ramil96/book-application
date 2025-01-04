from flask import render_template
from taskmanager import app, db
from taskmanager.models import Genre, Book, Review


@app.route("/")
def home():
    # Pass genres and books to the template to display on the home page
    genres = Genre.query.all()
    books = Book.query.all()
    return render_template("books.html", genres=genres, books=books)


@app.route("/add_book")
def add_book():
    # Render the "Add Book" page
    return render_template("add_book.html")


@app.route("/genres")
def genres():
    # Placeholder for genres page
    return render_template("genres.html")
