"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, Markup)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/movies')
def movies():
    movies = crud.get_movies()
    return render_template('all_movies.html', movies=movies)

@app.route('/movies/<movie_id>')
def show_movies(movie_id):
    movie = crud.get_movie_by_id(movie_id)

    return render_template('movie_details.html', movie=movie)

@app.route('/users')
def users():
    users = crud.get_users()
    return render_template('all_users.html', users=users)

@app.route('/users/<user_id>')
def show_user(user_id):
    user = crud.get_user_by_id(user_id)
    rate = crud.get_rating_by_user(user_id)
    

    return render_template('user_details.html', user=user, rating=rate)

@app.route('/users', methods=['POST'])
def user_registration():
    email = request.form.get('email')
    password = request.form.get('password')

    if crud.get_user_by_email(email):
        flash('User already exist, please try again')
    else:
        crud.create_user(email, password)
        flash('Account created successfully, please log in')
    
    return redirect('/')

@app.route('/login', methods=['POST'])
def user_login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user and password==user.password:
        session['user_id'] = user.user_id
        flash('Log in sucessful!')
    else:
        flash('Password inccorect, please try again')

    return redirect('/')

@app.route('/user-rating', methods=['POST'])
def user_rating():

    rating = int(request.form.get('rating'))
    movie_title = crud.get_movie_by_title(request.form.get('title'))
    flash(f'You have rated {movie_title.title}')
    flash(Markup(f'<a href="/users/{session["user_id"]}" class="alert-link">Take Me to My Ratings</a>'))

    current_user = crud.get_user_by_id(session['user_id'])

    movie_rating = crud.create_rating(current_user, movie_title, rating)
    current_user.rating.append(movie_rating)
    
    return redirect('/movies')


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
