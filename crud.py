"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def get_users():
    """Retuns all the users"""
    return User.query.all()

def get_user_by_id(user_id):
    """Returns user_id and email from User class"""

    return User.query.get(user_id)

def get_rating_by_user(user_id):
    """Returns all ratings from user"""
    user_ratings = []

    for user_rating in get_user_by_id(user_id).rating:
        user_ratings.append(user_rating)
    return user_ratings

def get_user_by_email(email):
    """Return a user by email"""
    
    return User.query.filter(User.email == email).first()

def create_movie(title, overview, release_date, poster_path):
    """Create and return a movie"""
    movie = Movie(title=title, overview=overview, release_date=release_date, poster_path=poster_path)

    db.session.add(movie)
    db.session.commit()

    return movie

def get_movies():
    """Returns all movies"""
    return Movie.query.all()

def get_movie_by_id(movie_id):
    """Return movie_id and title of movie from Movie class"""
    return Movie.query.get(movie_id)

def get_movie_by_title(title):
    """Returns the movie title from Movie class"""
    return Movie.query.filter(Movie.title==title).one()

def create_rating(user, movie, score):
    """Create a rating from user rating and movie rating"""

    rating = Rating(user=user, movie=movie, score=score)

    db.session.add(rating)
    db.session.commit()

    return rating

if __name__ == '__main__':
    from server import app
    connect_to_db(app)