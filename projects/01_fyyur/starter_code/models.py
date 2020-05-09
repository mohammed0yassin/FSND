from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
#----------------------------------------------------------------------------#
# DB Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'
    __searchable__= ["name","city","state","address"]
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String)) 
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120)) 
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False) 
    seeking_description = db.Column(db.String(500)) 
    # One-to-Many Relationship
    shows_ven = db.relationship('Show', backref='venue', passive_deletes=True) 
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
    shows_art = db.relationship('Show', backref='artist', passive_deletes=True)

    # DONE TODO: implement any missing fields, as a database migration using Flask-Migrate

class Show(db.Model):
  __tablename__='Show'
  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id', ondelete='cascade'))
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id', ondelete='cascade'))
  start_time = db.Column(db.DateTime, nullable=False)

    # DONE TODO: implement any missing fields, as a database migration using Flask-Migrate
