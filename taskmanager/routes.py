from flask import render_template, request, redirect, url_for
from taskmanager import app, db
from taskmanager.models import Genre, Book, Review  # Import models from models.py

@app.route("/")
def home():
    books = Book.query.order_by(Book.title).all()
    return render_template("books.html", books=books)

@app.route("/genres")
def genres():
    genres = Genre.query.order_by(Genre.genre_name).all()
    return render_template("genres.html", genres=genres)

@app.route("/add_genre", methods=["GET", "POST"])
def add_genre():
    if request.method == "POST":
        genre_name = request.form.get("genre_name")
        genre = Genre(genre_name=genre_name)
        db.session.add(genre)
        db.session.commit()
        return redirect(url_for("genres"))
    return render_template("add_genre.html")

@app.route("/edit_genre/<int:genre_id>", methods=["GET", "POST"])
def edit_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    if request.method == "POST":
        genre.genre_name = request.form.get("genre_name")
        db.session.commit()
        return redirect(url_for("genres"))
    return render_template("edit_genre.html", genre=genre)

@app.route("/delete_genre/<int:genre_id>", methods=["POST"])
def delete_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    db.session.delete(genre)
    db.session.commit()
    return redirect(url_for("genres"))

@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        book_title = request.form.get("book_title")
        author_name = request.form.get("author_name")
        book_description = request.form.get("book_description")
        genre_id = request.form.get("genre_id")

        book = Book(
            title=book_title,
            author=author_name,
            description=book_description,
            genre_id=genre_id
        )
        db.session.add(book)
        db.session.commit()

        return redirect(url_for("home"))

    genres = Genre.query.order_by(Genre.genre_name).all()
    return render_template("add_book.html", genres=genres)

@app.route("/edit_book/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == "POST":
        book.title = request.form.get("title")
        book.genre_id = request.form.get("genre_id")
        db.session.commit()
        return redirect(url_for("home"))
    genres = Genre.query.order_by(Genre.genre_name).all()
    return render_template("edit_book.html", book=book, genres=genres)

@app.route("/delete_book/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/reviews")
def reviews():
    # Implement the logic to retrieve reviews
    reviews = Review.query.all()  # This can be customized as per your needs
    return render_template("reviews.html", reviews=reviews)
