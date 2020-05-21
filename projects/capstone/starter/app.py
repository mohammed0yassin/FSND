import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, setup_db, Movie, Actor, Show
from datetime import datetime
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  return app

app = create_app()

CORS(app, resources={r"*": {"origins": "*"}})


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,PATCH')
    return response


'''
Get '/shows': a Public endpoint for anyone to view the movies of the agency
'''
@app.route('/shows')
def view_shows():
  no_shows_all = db.session.query(Show.movie_id).distinct().count() # number of shows
  movies_in_shows = [value for value, in db.session.query(Show.movie_id).distinct().all()]
  data = []
  for cur_show in range(no_shows_all):
    cur_movie = Movie.query.get(movies_in_shows[cur_show])# current movie
    cur_actors = db.session.query(Actor).join(Show).filter(Show.movie_id==cur_movie.id).all() # actors in the current movie
    artist_record = []
    for actor in range(len(cur_actors)):
      current_actor = cur_actors[actor]
      artist_info = {
        'id': current_actor.id,
        'name': current_actor.name,
        'age': current_actor.age,
        'gender': current_actor.gender
      }
      artist_record.append(artist_info)


    record = {
      'movie_title': cur_movie.title,
      'movie_id': cur_movie.id,
      'Artists': artist_record,
      'release_date': cur_movie.release_date
    }
    data.append(record)
  return jsonify(data)

  # db.session.query(Actor).join(Show).filter(Show.movie_id==1).all() # artists in this movie









if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)