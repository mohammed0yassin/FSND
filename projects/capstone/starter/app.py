import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, setup_db, Movie, Actor, Show
from datetime import datetime
from auth import AuthError, requires_auth


'''
def list_shows():
  it lists all the shows of the agencys
  returns shows which is a dictionary that has the shows
'''


def list_shows():
  # number of shows
  no_shows_all = db.session.query(Show.movie_id).distinct().count()
  movies_not_formatted = db.session.query(Show.movie_id).distinct().all()
  movies_in_shows = [value for value, in movies_not_formatted]
  shows = []
  for cur_show in range(no_shows_all):
    # current movie
    cur_movie = Movie.query.get(movies_in_shows[cur_show])
    # actors in the current movie
    cur_actors = db.session.query(Actor).join(Show) \
                   .filter(Show.movie_id == cur_movie.id).all()
    actor_record = []
    for actor in range(len(cur_actors)):
      current_actor = cur_actors[actor]
      actor_info = {
        'id': current_actor.id,
        'name': current_actor.name,
        'age': current_actor.age,
        'gender': current_actor.gender
      }
      actor_record.append(actor_info)

    record = {
      'movie_title': cur_movie.title,
      'movie_id': cur_movie.id,
      'Actors': actor_record,
      'release_date': cur_movie.release_date
    }
    shows.append(record)
  return shows


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  CORS(app, resources={r"*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers',
                           'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods',
                           'GET,PUT,POST,DELETE,PATCH')
      return response

  '''
  GET '/shows': a public endpoint for anyone to view the shows of the agency
  '''
  @app.route('/shows')
  def view_shows():
    try:
      shows = list_shows()
      return jsonify({
        'success': True,
        'shows': shows
      })
    except:
      abort(422)
  '''
  GET '/actors': an endpoint to view the actors of the agency
    requires permission 'get:actors'
  '''
  @app.route('/actors')
  @requires_auth('get:actors')
  def view_actors(payload):
    actors_all = Actor.query.all()
    actors = [actor.format() for actor in actors_all]
    if len(actors) == 0:
      abort(404)
    return jsonify({
      'success': True,
      'actors': actors
    })

  '''
  GET '/movies': an endpoint to view the movies of the agency
    requires permission 'get:movies'
  '''
  @app.route('/movies')
  @requires_auth('get:movies')
  def view_movies(payload):
    movies_all = Movie.query.all()
    movies = [movie.format() for movie in movies_all]
    if len(movies) == 0:
      abort(404)
    return jsonify({
      'success': True,
      'movies': movies
    })

  '''
  POST '/actors': An endpoint that adds a new actor
    requires permission 'post:actors'
  '''
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def add_actor(payload):
    try:
      body = request.get_json()
      actor_data = {
        'name': body['name'],
        'age': body['age'],
        'gender': body['gender']
      }

      new_actor = Actor(**actor_data)
      new_actor.insert()

      actors_all = Actor.query.all()
      actors = [actor.format() for actor in actors_all]

      return jsonify({
        'success': True,
        'actors': actors
      })
    except:
      abort(422)

  '''
  POST '/movies': An endpoint that adds a new movie
    requires permission 'post:movies'
  '''
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def add_movie(payload):
    try:
      body = request.get_json()
    # release_date format: '%Y-%m-%d %H:%M:%S' #example: "2019-05-21 21:30:00"
      date_not_formatted = body['release_date']
      date_formatted = datetime.strptime(date_not_formatted,
                                         '%Y-%m-%d %H:%M:%S')
      movie_data = {
        'title': body['title'],
        'release_date': date_formatted
      }

      new_movie = Movie(**movie_data)
      new_movie.insert()

      movies_all = Movie.query.all()
      movies = [movie.format() for movie in movies_all]

      return jsonify({
        'success': True,
        'movies': movies
      })
    except:
      abort(422)

  '''
  POST '/shows': an end point to add a new show
    requires permission 'post:shows'
  '''
  @app.route('/shows', methods=['POST'])
  @requires_auth('post:shows')
  def add_show(payload):
    try:
      body = request.get_json()
      show_data = {
        'movie_id': body['movie_id'],
        'actors_ids': body['actors_ids']
      }
      # check if a show with this movie already exists
      check_movie = Show.query.filter(Show.movie_id ==
                                      show_data['movie_id']).all()
      if check_movie:  # if check_movie has a movie
        abort(400)
      no_of_actors = len(show_data['actors_ids'])
      for actor in range(no_of_actors):
        new_show = Show(movie_id=show_data['movie_id'],
                        actor_id=show_data['actors_ids'][actor])
        new_show.insert()

      shows = list_shows()

      return jsonify({
        'success': True,
        'shows': shows
      })
    except:
      abort(422)

  '''
  PATCH '/actors/<id>': An endpoint to edit an actor
    requires permission 'patch:actors'
  '''
  @app.route('/actors/<id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def edit_actor(payload, id):
    try:
      body = request.get_json()
      new_name = body.get('name', None)
      new_age = body.get('age', None)
      new_gender = body.get('gender', None)

      current_actor = Actor.query.get(id)

      if new_name is not None:
        current_actor.name = new_name
      if new_age is not None:
        current_actor.age = new_age
      if new_gender is not None:
        current_actor.gender = new_gender

      current_actor.update()

      actors_all = Actor.query.all()
      actors = [actor.format() for actor in actors_all]

      return jsonify({
        'success': True,
        'edited': id,
        'actors': actors
      })
    except:
      abort(422)

  '''
  PATCH '/movies/<id>': An endpoint to edit a movie
    requires permission 'patch:movies'
  '''
  @app.route('/movies/<id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def edit_movie(payload, id):
    try:
      body = request.get_json()
      new_title = body.get('title', None)
    # release_date format: '%Y-%m-%d %H:%M:%S' #example: "2019-05-21 21:30:00"
      date_not_formatted = body.get('release_date', None)

      current_movie = Movie.query.get(id)

      if new_title is not None:
        current_movie.title = new_title
      if date_not_formatted is not None:
        date_formatted = datetime.strptime(date_not_formatted,
                                           '%Y-%m-%d %H:%M:%S')
        current_movie.release_date = date_formatted

      current_movie.update()

      movies_all = Movie.query.all()
      movies = [movie.format() for movie in movies_all]

      return jsonify({
        'success': True,
        'edited': id,
        'movies': movies
      })
    except:
      abort(422)

  '''
  DELETE '/actors/<id>': an endpoint to delete an actor
    requires permission 'delete:actors'
  '''
  @app.route('/actors/<id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, id):
    select_actor = Actor.query.get(id)

    if select_actor is None:
      abort(404)

    select_actor.delete()

    actors_all = Actor.query.all()
    actors = [actor.format() for actor in actors_all]

    return jsonify({
      'success': True,
      'deleted': id,
      'actors': actors
    })

  '''
  DELETE '/movies/<id>': an endpoint to delete an movie
    requires permission 'delete:movies'
  '''
  @app.route('/movies/<id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, id):
    select_movie = Movie.query.get(id)
    if select_movie is None:
      abort(404)

    select_movie.delete()

    movies_all = Movie.query.all()
    movies = [movie.format() for movie in movies_all]

    return jsonify({
      'success': True,
      'deleted': id,
      'movies': movies
    })

  '''
  DELETE '/shows/<movie_id>': an endpoint to delete a show using its movie_id
    requires permission 'delete:shows'
  '''
  @app.route('/shows/<movie_id>', methods=['DELETE'])
  @requires_auth('delete:shows')
  def delete_show(payload, movie_id):
    selected_show = Show.query.filter(Show.movie_id == movie_id).all()
    if not selected_show:  # if no shows with this movie exist, abort
      abort(404)
    for show in selected_show:
      show.delete()

    shows = list_shows()
    return jsonify({
      'success': True,
      'deleted': movie_id,
      'shows': shows
    })

  '''
  Error handlers
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'Bad Request'
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Resource Not Found'
    }), 404

  @app.errorhandler(422)
  def unproccessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'Unproccessable'
    }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': 'Internal Server Error'
    }), 500

  @app.errorhandler(AuthError)
  def autherror(error):
      error_details = error.error
      error_status_code = error.status_code
      return jsonify({
          'success': False,
          'error': error_status_code,
          'message': error_details['description']
      }), error_status_code
  return app

app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
