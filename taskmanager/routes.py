from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from taskmanager import app, db
from taskmanager.models import Genre, Book, Review, User
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)

# Load user for flask-login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully!", "success")
            
            # Redirect based on user role
            if user.role == 'admin':
                return redirect(url_for("admin_dashboard"))  # Change to admin page route
            else:
                return redirect(url_for("home"))
        else:
            flash("Invalid email or password.", "error")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect(url_for("home"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")

        # Basic validation
        if not username or not email or not password:
            flash("Please fill in all fields.", "error")
        elif password != password_confirm:
            flash("Passwords do not match.", "error")
        else:
            # Check if the user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("Email already exists. Please login.", "error")
            else:
                user = User(username=username, email=email, role='user')
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                flash("Account created successfully!", "success")
                return redirect(url_for("login"))
    
    return render_template("register.html")

# Home Page
@app.route("/")
def home():
    books = Book.query.order_by(Book.title).all()
    return render_template("books.html", books=books)

# Genres
@app.route("/genres")
def genres():
    genres = Genre.query.order_by(Genre.genre_name).all()
    return render_template("genres.html", genres=genres)

@app.route("/add_genre", methods=["GET", "POST"])
def add_genre():
    if request.method == "POST":
        genre_name = request.form.get("genre_name")
        if not genre_name:
            flash("Genre name is required!", "error")
        else:
            genre = Genre(genre_name=genre_name)
            db.session.add(genre)
            db.session.commit()
            flash("Genre added successfully!", "success")
            return redirect(url_for("genres"))
    return render_template("add_genre.html")

@app.route("/edit_genre/<int:genre_id>", methods=["GET", "POST"])
def edit_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    if request.method == "POST":
        genre_name = request.form.get("genre_name")
        if not genre_name:
            flash("Genre name cannot be empty!", "error")
        else:
            genre.genre_name = genre_name
            db.session.commit()
            flash("Genre updated successfully!", "success")
            return redirect(url_for("genres"))
    return render_template("edit_genre.html", genre=genre)

@app.route("/delete_genre/<int:genre_id>", methods=["POST"])
def delete_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    db.session.delete(genre)
    db.session.commit()
    flash("Genre deleted successfully!", "success")
    return redirect(url_for("genres"))

# Books
@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        book_title = request.form.get("book_title")
        author_name = request.form.get("author_name")
        book_description = request.form.get("book_description")
        genre_id = request.form.get("genre_id")

        if not book_title or not genre_id:
            flash("Book title and genre are required!", "error")
        else:
            book = Book(
                title=book_title,
                author=author_name,
                description=book_description,
                genre_id=genre_id
            )
            db.session.add(book)
            db.session.commit()
            flash("Book added successfully!", "success")
            return redirect(url_for("home"))

    genres = Genre.query.order_by(Genre.genre_name).all()
    return render_template("add_book.html", genres=genres)

@app.route("/edit_book/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == "POST":
        book_title = request.form.get("title")
        genre_id = request.form.get("genre_id")
        if not book_title or not genre_id:
            flash("Book title and genre cannot be empty!", "error")
        else:
            book.title = book_title
            book.genre_id = genre_id
            db.session.commit()
            flash("Book updated successfully!", "success")
            return redirect(url_for("home"))
    genres = Genre.query.order_by(Genre.genre_name).all()
    return render_template("edit_book.html", book=book, genres=genres)

@app.route("/delete_book/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash("Book deleted successfully!", "success")
    return redirect(url_for("home"))

# Reviews
@app.route("/reviews", methods=["GET", "POST"])
def reviews():
    genre_id = request.args.get("genre_id", None)
    books = Book.query.all()  # Get all books to populate the dropdown
    if genre_id:
        reviews = Review.query.join(Book).filter(Book.genre_id == genre_id).all()
    else:
        reviews = Review.query.all()
    genres = Genre.query.order_by(Genre.genre_name).all()

    return render_template("reviews.html", reviews=reviews, genres=genres, books=books)

# reviews
@app.route('/add_review', methods=['GET', 'POST'])
def add_review():
    book_id = request.form.get('book_id')  # Get book_id from the form
    rating = request.form.get('rating')
    review_text = request.form.get('review_text')

    if not book_id or not rating or not review_text:
        flash("All fields are required!", "error")
        return redirect(url_for('reviews'))

    # Save the review to the database
    book = Book.query.get(book_id)
    if not book:
        flash("Book not found!", "error")
        return redirect(url_for('reviews'))

    review = Review(book_id=book_id, rating=rating, review_text=review_text)
    db.session.add(review)
    db.session.commit()
    flash("Review added successfully!", "success")
    return redirect(url_for('reviews'))

# book details
@app.route("/book/<int:book_id>")
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    reviews = Review.query.filter_by(book_id=book_id).all()
    return render_template("book_detail.html", book=book, reviews=reviews)

@app.route("/edit_review/<int:review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)

    if request.method == "POST":
        review_text = request.form.get("review_text")
        rating = request.form.get("rating")
        if not review_text or not rating:
            flash("Review text and rating cannot be empty!", "error")
        else:
            review.review_text = review_text
            review.rating = rating
            db.session.commit()
            flash("Review updated successfully!", "success")
            return redirect(url_for("book_detail", book_id=review.book_id))

    return render_template("edit_review.html", review=review)

@app.route("/delete_review/<int:review_id>", methods=["POST"])
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)

    db.session.delete(review)
    db.session.commit()
    flash("Review deleted successfully!", "success")
    return redirect(url_for("book_detail", book_id=review.book_id))

@app.route("/genres/<int:genre_id>")
def genre_books(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    books = Book.query.filter_by(genre_id=genre_id).order_by(Book.title).all()
    return render_template("genre_books.html", genre=genre, books=books)
