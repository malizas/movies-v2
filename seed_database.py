"""Automatically seed into database"""

import os
import json
from random import choice, randint
from datetime import datetime
import crud, model, server

os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

movies_in_db = []
for movie in movie_data:
    title, overview, poster_path = movie["title"], movie["overview"], movie["poster_path"]
    date = movie["release_date"]
    format = '%Y-%m-%d'
    release_date = datetime.strptime(date, format)

    movie_to_add = crud.create_movie(title, overview, release_date, poster_path)
    print(f' movie to add type: {type(movie_to_add)}')
    movies_in_db.append(movie_to_add)

for n in range(11,12):
    email = f'user{n}@test.com'
    password = 'test'

    user_to_add = crud.create_user(email, password)
    print(f'user to add type: {type(user_to_add)}')
    for num in range(2):
        movie_to_rate = choice(movies_in_db)
        random_rating = randint(1, 5)
        
        crud.create_rating(user_to_add, movie_to_rate, random_rating)