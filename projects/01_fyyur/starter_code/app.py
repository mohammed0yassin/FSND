#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from datetime import datetime
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# DONE TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'
    __searchable__= ["name","city","state","address"]
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String)) # Added
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120)) #Added
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False) #Added
    seeking_description = db.Column(db.String(500)) #Added
    # One-to-Many Relationship
    shows_ven = db.relationship('Show', backref='venue') #Added
    past_shows_count = db.Column(db.Integer) #Added

    # DONE TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'
    __searchable__= ["name","city","state"]
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String())
    # One-to-Many Relationship
    shows_art = db.relationship('Show', backref='artist')

    # DONE TODO: implement any missing fields, as a database migration using Flask-Migrate

class Show(db.Model):
  __tablename__='Show'
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
  start_time = db.Column(db.DateTime, nullable=False)

# DONE TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#  ----------------------------------------------------------------
# Adding data to database for the first run only
#  ----------------------------------------------------------------

if Show.query.first() == None:
# Venues data
  datav1={
      "id": 1,
      "name": "The Musical Hop",
      "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
      "address": "1015 Folsom Street",
      "city": "San Francisco",
      "state": "CA",
      "phone": "123-123-1234",
      "website": "https://www.themusicalhop.com",
      "facebook_link": "https://www.facebook.com/TheMusicalHop",
      "seeking_talent": True,
      "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
      "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  datav2={
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "genres": ["Classical", "R&B", "Hip-Hop"],
      "address": "335 Delancey Street",
      "city": "New York",
      "state": "NY",
      "phone": "914-003-1132",
      "website": "https://www.theduelingpianos.com",
      "facebook_link": "https://www.facebook.com/theduelingpianos",
      "seeking_talent": False,
      "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80"
  }
  datav3={
      "id": 3,
      "name": "Park Square Live Music & Coffee",
      "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
      "address": "34 Whiskey Moore Ave",
      "city": "San Francisco",
      "state": "CA",
      "phone": "415-000-1234",
      "website": "https://www.parksquarelivemusicandcoffee.com",
      "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
      "seeking_talent": False,
      "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80"
  }
  venue_data1 = Venue(**datav1)
  venue_data2 = Venue(**datav2)
  venue_data3 = Venue(**datav3)
  db.session.add_all([venue_data1, venue_data2, venue_data3])
  # END of Venues data

  # Artists data
  dataa1={
      "id": 4,
      "name": "Guns N Petals",
      "genres": ["Rock n Roll"],
      "city": "San Francisco",
      "state": "CA",
      "phone": "326-123-5000",
      "website": "https://www.gunsnpetalsband.com",
      "facebook_link": "https://www.facebook.com/GunsNPetals",
      "seeking_venue": True,
      "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
      "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  dataa2={
      "id": 5,
      "name": "Matt Quevedo",
      "genres": ["Jazz"],
      "city": "New York",
      "state": "NY",
      "phone": "300-400-5000",
      "facebook_link": "https://www.facebook.com/mattquevedo923251523",
      "seeking_venue": False,
      "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80"
  }
  dataa3={
      "id": 6,
      "name": "The Wild Sax Band",
      "genres": ["Jazz", "Classical"],
      "city": "San Francisco",
      "state": "CA",
      "phone": "432-325-5432",
      "seeking_venue": False,
      "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80"
  }
  arist_data1 = Artist(**dataa1)
  arist_data2 = Artist(**dataa2)
  arist_data3 = Artist(**dataa3)
  db.session.add_all([arist_data1, arist_data2, arist_data3])
  db.session.commit()
 # END of Artists data

  # Shows Data
  show_data1 = Show(venue_id = 1, artist_id = 4, start_time = "2019-05-21T21:30:00.000Z" )
  db.session.add(show_data1)
  db.session.commit()
  show_data2 = Show(venue_id = 3, artist_id = 5, start_time = "2019-06-15T23:00:00.000Z" )
  db.session.add(show_data2)
  db.session.commit()
  show_data3 = Show(venue_id = 3, artist_id = 6, start_time = "2035-04-01T20:00:00.000Z" )
  db.session.add(show_data3)
  db.session.commit()
  show_data4 = Show(venue_id = 3, artist_id = 6, start_time = "2035-04-08T20:00:00.000Z" )
  db.session.add(show_data4)
  db.session.commit()
  show_data5 = Show(venue_id = 3, artist_id = 6, start_time = "2035-04-15T20:00:00.000Z" )
  db.session.add(show_data5)
  db.session.commit()
  # END of Shows data

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  ----------------------------------------------------------------
#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # DONE TODO: replace with real venues data.
  #    DONE TODO   num_shows should be aggregated based on number of upcoming shows per venue.
  locations = Venue.query.distinct('city','state').all()
  data = []
  for location in locations:
    venues = Venue.query.filter(Venue.city == location.city, Venue.state == location.state).all()
    venue_record = []
    for venue in range(len(venues)):
      venue_id = venues[venue].id
      venue_name = venues[venue].name
      num_shows = Show.query.filter(Show.venue_id == venue_id, Show.start_time > datetime.now()).count()
      venue_info = {
        "id": venue_id,
        "name": venue_name,
        "num_upcoming_shows": num_shows,  
      }
      venue_record.append(venue_info)
    record = {
      'city': location.city,
      'state': location.state,
      'venues': venue_record
    }
    data.append(record)
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # DONE TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term =  request.form.get('search_term', '')
  results =  Venue.query.filter(Venue.name.ilike("%"+search_term+"%")).all()
  result_count = Venue.query.filter(Venue.name.ilike("%"+search_term+"%")).count()
  rdata = []
  for result in range(len(results)):
    num_upcoming_shows = Show.query.filter(Show.venue_id == results[result].id, Show.start_time > datetime.now()).count()
    record = {
      "id": results[result].id,
      "name": results[result].name,
      "num_upcoming_shows": num_upcoming_shows,
    }
    rdata.append(record)

  response={
    "count": result_count,
    "data": rdata
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # DONE TODO: replace with real venue data from the venues table, using venue_id
  current_venue = Venue.query.get(venue_id)
  num_past_shows = Show.query.filter(Show.venue_id == venue_id, Show.start_time < datetime.now()).count()
  num_upcoming_shows = Show.query.filter(Show.venue_id == venue_id, Show.start_time > datetime.now()).count()
  past_shows_record = []
  upcoming_shows_record = []
  data = []
  for num_pshow in range(num_past_shows):
    artist = Show.query.filter(Show.venue_id == venue_id, Show.start_time < datetime.now())[num_pshow]
    artist_data = Artist.query.get(artist.artist_id)
    precord = {
      "artist_id": artist_data.id,
      "artist_name": artist_data.name,
      "artist_image_link": artist_data.image_link,
      "start_time": artist.start_time.strftime("%Y/%m/%d, %H:%M:%S")
    }
    past_shows_record.append(precord)

  for num_ushow in range(num_upcoming_shows):
    artist = Show.query.filter(Show.venue_id == 3, Show.start_time > datetime.now())[num_ushow]
    artist_data = Artist.query.get(artist.artist_id)
    urecord = {
      "artist_id": artist_data.id,
      "artist_name": artist_data.name,
      "artist_image_link": artist_data.image_link,
      "start_time": artist.start_time.strftime("%Y/%m/%d, %H:%M:%S")
    }
    upcoming_shows_record.append(urecord)  

  data={
    "id": venue_id,
    "name": current_venue.name,
    "genres": current_venue.genres,
    "address": current_venue.address,
    "city": current_venue.city,
    "state": current_venue.state,
    "phone": current_venue.phone,
    "website": current_venue.website,
    "facebook_link": current_venue.facebook_link,
    "seeking_talent": current_venue.seeking_talent,
    "seeking_description": current_venue.seeking_description,
    "image_link": current_venue.image_link,
    "past_shows": past_shows_record,
    "upcoming_shows": upcoming_shows_record,
    "past_shows_count": num_past_shows,
    "upcoming_shows_count": num_upcoming_shows,
  }
  data = list(filter(lambda d: d['id'] == venue_id, [data]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # DONE TODO: insert form data as a new Venue record in the db, instead
  # DONE TODO: modify data to be the data object returned from db insertion
    error = False
    try:
        venue = Venue()
        venue.name = request.form['name']
        venue.city = request.form['city']
        venue.state = request.form['state']
        venue.address = request.form['address']
        venue.phone = request.form['phone']
        venue.genres = request.form.getlist('genres')
        venue.facebook_link = request.form['facebook_link']
        db.session.add(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            flash('An error occured. Venue ' + request.form['name'] + ' Could not be listed!')
        else:
            flash('Venue ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')
  # on successful db insert, flash success
  # flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # DONE TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # DONE TODO: replace with real data returned from querying the database
  artists = Artist.query.all()
  data = []
  for artist in range(len(artists)):
    artist_id = artists[artist].id 
    artist_name = artists[artist].name 
    record = {
      "id": artist_id,
      "name": artist_name
    }
    data.append(record) 
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # DONE TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term =  request.form.get('search_term', '')
  results =  Artist.query.filter(Artist.name.ilike("%"+search_term+"%")).all()
  result_count = Artist.query.filter(Artist.name.ilike("%"+search_term+"%")).count()
  rdata = []
  for result in range(len(results)):
    num_upcoming_shows = Show.query.filter(Show.artist_id == results[result].id, Show.start_time > datetime.now()).count()
    record = {
      "id": results[result].id,
      "name": results[result].name,
      "num_upcoming_shows": num_upcoming_shows,
    }
    rdata.append(record)

  response={
    "count": result_count,
    "data": rdata
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # DONE TODO: replace with real venue data from the venues table, using venue_id
  current_artist = Artist.query.get(artist_id)
  num_past_shows = Show.query.filter(Show.artist_id == artist_id, Show.start_time < datetime.now()).count()
  num_upcoming_shows = Show.query.filter(Show.artist_id == artist_id, Show.start_time > datetime.now()).count()
  past_shows_record = []
  upcoming_shows_record = []
  data = []
  if num_past_shows != 0:
    for num_pshow in range(num_past_shows):
      venue = Show.query.filter(Show.artist_id == artist_id, Show.start_time < datetime.now())[num_pshow]
      venue_data = Venue.query.get(venue.venue_id)
      precord = {
        "venue_id": venue_data.id,
        "venue_name": venue_data.name,
        "venue_image_link": venue_data.image_link,
        "start_time": venue.start_time.strftime("%Y/%m/%d, %H:%M:%S")
      }
      past_shows_record.append(precord)
      
  if num_upcoming_shows != 0:
    for num_ushow in range(num_upcoming_shows):
      venue = Show.query.filter(Show.artist_id == artist_id, Show.start_time > datetime.now())[num_ushow]
      venue_data = Venue.query.get(venue.venue_id)
      urecord = {
        "venue_id": venue_data.id,
        "venue_name": venue_data.name,
        "venue_image_link": venue_data.image_link,
        "start_time": venue.start_time.strftime("%Y/%m/%d, %H:%M:%S")
      }
      upcoming_shows_record.append(urecord)  
  
  data={
    "id": current_artist.id,
    "name": current_artist.name,
    "genres": current_artist.genres,
    "city": current_artist.city,
    "state": current_artist.state,
    "phone": current_artist.phone,
    "website": current_artist.website,
    "facebook_link": current_artist.facebook_link,
    "seeking_venue": current_artist.seeking_venue,
    "seeking_description": current_artist.seeking_description,
    "image_link": current_artist.image_link,
    "past_shows": past_shows_record,
    "upcoming_shows": upcoming_shows_record,
    "past_shows_count": num_past_shows,
    "upcoming_shows_count": num_upcoming_shows,
  }

  data = list(filter(lambda d: d['id'] == artist_id, [data]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # DONE TODO: insert form data as a new Venue record in the db, instead
  # DONE TODO: modify data to be the data object returned from db insertion
  error = False
  try:
      artist = Artist()
      artist.name = request.form['name']
      artist.city = request.form['city']
      artist.state = request.form['state']
      artist.phone = request.form['phone']
      artist.genres = request.form.getlist('genres')
      artist.facebook_link = request.form['facebook_link']
      db.session.add(artist)
      db.session.commit()
  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
  finally:
      db.session.close()
      if error:
          flash('An error occured. Artist ' + request.form['name'] + ' Could not be listed!')
      else:
          flash('Artist ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')
  # on successful db insert, flash success
  # flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # DONE TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')



#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # DONE TODO: replace with real venues data.
  #   DONE TODO num_shows should be aggregated based on number of upcoming shows per venue.
  shows = Show.query.all()
  data = []
  for show in range(len(shows)):
    venue = Venue.query.get(shows[show].venue_id)
    artist = Artist.query.get(shows[show].artist_id)
    record = {
    "venue_id": venue.id,
    "venue_name": venue.name,
    "artist_id": artist.id,
    "artist_name": artist.name,
    "artist_image_link": artist.image_link,
    "start_time": shows[show].start_time.strftime("%Y/%m/%d, %H:%M:%S")
    }
    data.append(record)
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
