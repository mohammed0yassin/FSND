import os
from sqlalchemy import Column, String, Integer, ARRAY, DateTime, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from dotenv import load_dotenv
load_dotenv() # https://www.nylas.com/blog/making-use-of-environment-variables-in-python/

database_name = "agency"
database_path = os.environ['DATABASE_URL']
# database_path = "postgres://{}:{}@{}/{}".format('postgres','12345678','localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()

'''
Movie
'''
class Movie(db.Model):
    __tablename__= 'Movie'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(DateTime, nullable=False)
    # One-to-Many Relationship
    shows_movie = db.relationship('Show', backref='movie', passive_deletes=True) 
    

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

'''
Actor
'''
class Actor(db.Model):
    __tablename__= 'Actor'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    # One-to-Many Relationship
    shows_actor = db.relationship('Show', backref='actor', passive_deletes=True)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

'''
Show
'''

class Show(db.Model):
    __tablename__='Show'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, db.ForeignKey('Movie.id', ondelete='cascade'))
    actor_id = Column(Integer, db.ForeignKey('Actor.id', ondelete='cascade'))
        
    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'actor_id': self.actor_id
        }