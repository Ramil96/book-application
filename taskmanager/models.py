from taskmanager import db

class Genre(db.Model):
    __tablename__ = "genre"
    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(25), unique=True, nullable=False)
    books = db.relationship("Book", backref="genre", cascade="all, delete", lazy=True)

    def __repr__(self):
        return self.genre_name


class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"), nullable=False)
    reviews = db.relationship("Review", backref="book", cascade="all, delete", lazy=True)

    def __repr__(self):
        return f"Book: {self.title} by {self.author}"


class Review(db.Model):
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True)
    review_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)

    def __repr__(self):
        return f"Review: {self.rating} stars | {self.review_text[:30]}..."
