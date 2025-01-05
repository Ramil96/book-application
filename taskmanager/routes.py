from flask import render_template, request, redirect, url_for
from taskmanager import app, db
from taskmanager.models import Genre, Book


@app.route("/")
def home():
    genres = Genre.query.all()
    books = Book.query.all()
    return render_template("books.html", genres=genres, books=books)


@app.route("/genres")
def genres():
    genres = Genre.query.all()
    return render_template("genres.html", genres=genres)


@app.route("/add_genre", methods=["GET", "POST"])
def add_genre():
    if request.method == "POST":
        # Create a new genre using the form data
        genre = Genre(genre_name=request.form.get("genre_name"))
        db.session.add(genre)
        db.session.commit()
        return redirect(url_for("genres"))
    return render_template("add_genre.html")
