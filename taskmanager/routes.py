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

@app.route("/reviews", methods=["GET", "POST"])
def reviews():
    genre_id = request.args.get("genre_id")
    genres = Genre.query.order_by(Genre.genre_name).all()
    books = Book.query.order_by(Book.title).all()

    if genre_id:
        reviews = Review.query.join(Book).filter(Book.genre_id == genre_id).all()
    else:
        reviews = Review.query.order_by(Review.id).all()

    return render_template("reviews.html", reviews=reviews, genres=genres, books=books)



@app.route("/book/<int:book_id>/add_review", methods=["GET", "POST"])
def add_review(book_id):
    book = Book.query.get_or_404(book_id)
    
    if request.method == "POST":
        review_text = request.form.get("review_text")
        rating = request.form.get("rating")
        
        # Create a new review
        review = Review(review_text=review_text, rating=rating, book_id=book_id)
        db.session.add(review)
        db.session.commit()
        
        return redirect(url_for("book_detail", book_id=book_id))
    
    return render_template("add_review.html", book=book)




@app.route("/book/<int:book_id>")
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    reviews = Review.query.filter_by(book_id=book_id).all()  # Fetch reviews for the specific book
    return render_template("book_detail.html", book=book, reviews=reviews)


@app.route("/genre/<int:genre_id>")
def genre_books(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    return render_template("genre_books.html", genre=genre)

