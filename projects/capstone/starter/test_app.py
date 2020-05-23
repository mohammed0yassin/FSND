import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie, Show

from dotenv import load_dotenv
load_dotenv() # https://www.nylas.com/blog/making-use-of-environment-variables-in-python/

exec_producer_token = os.environ['exec_producer_token']
casting_director_token = os.environ['casting_director_token']
casting_assistant_token = os.environ['casting_assistant_token']

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.exec_producer_headers = {"Authorization": "Bearer {}".format(exec_producer_token)}
        self.casting_director_headers = {"Authorization": "Bearer {}".format(casting_director_token)}
        self.casting_assistant_headers = {"Authorization": "Bearer {}".format(casting_assistant_token)}
        self.database_name = "agency_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','12345678','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_actor = {
            'name': 'Unittest Actor',
            'age': 20,
            'gender': 'Male'
        }

        self.edit_actor = {
            'name': 'Edited Unittest Actor',
            'age': 25,
            'gender': 'Male'
        }

        self.new_movie = {
            'title': 'Unittest Movie',
            'release_date': "2025-09-15 15:30:00",
        }

        self.edit_movie = {
            'title': 'Edited Unittest Movie',
            'release_date': "2026-10-10 20:20:00",
        }

        self.new_show = {
            'movie_id': 3,
            'actors_ids': [1,2]
        }
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            #self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass


    '''
    Actors Tests
    '''

    # -----------------------
    # GET '/actors'
    # -----------------------
    def test_view_actors_no_headers(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Authorization header is expected.")

    def test_view_actors_casting_assistant(self):
        res = self.client().get('/actors', headers=self.casting_assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_view_actors_casting_director(self):
        res = self.client().get('/actors', headers=self.casting_director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_view_actors_executive_producer(self):
        res = self.client().get('/actors', headers=self.exec_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    # -----------------------
    # POST '/actors'
    # -----------------------
    def test_add_actor_no_headers(self):
        res = self.client().post('/actors', json = self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Authorization header is expected.")

    def test_add_actors_casting_assistant(self):
        res = self.client().post('/actors', headers=self.casting_assistant_headers, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "the current user has insufficient permissions to perform the requested operation.")

    def test_add_actors_casting_director(self):
        res = self.client().post('/actors', headers=self.casting_director_headers, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_add_actors_executive_producer(self):
        res = self.client().post('/actors', headers=self.exec_producer_headers, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    # -----------------------
    # PATCH '/actors'
    # -----------------------
    def test_edit_actor_no_headers(self):
        res = self.client().patch('/actors/2', json = self.edit_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Authorization header is expected.")

    def test_edit_actors_casting_assistant(self):
        res = self.client().patch('/actors/2', headers=self.casting_assistant_headers, json=self.edit_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "the current user has insufficient permissions to perform the requested operation.")

    def test_edit_actors_casting_director(self):
        res = self.client().patch('/actors/4', headers=self.casting_director_headers, json=self.edit_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))
        
    def test_edit_actors_executive_producer(self):
        res = self.client().patch('/actors/5', headers=self.exec_producer_headers, json=self.edit_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    # -----------------------
    # DELETE '/actors'
    # -----------------------
    def test_delete_actor_no_headers(self):
        res = self.client().delete('/actors/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Authorization header is expected.")

    def test_delete_actors_casting_assistant(self):
        res = self.client().delete('/actors/2', headers=self.casting_assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "the current user has insufficient permissions to perform the requested operation.")

    def test_delete_actors_casting_director(self):
        res = self.client().delete('/actors/6', headers=self.casting_director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], '6')
        self.assertTrue(len(data['actors']))

    def test_delete_actors_executive_producer(self):
        res = self.client().delete('/actors/7', headers=self.exec_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], '7')
        self.assertTrue(len(data['actors']))
    '''
    Movies Tests
    '''
    def test_view_movies_no_headers(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Authorization header is expected.")

    def test_view_movies_casting_assistant(self):
        res = self.client().get('/movies', headers=self.casting_assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_view_movies_casting_director(self):
        res = self.client().get('/movies', headers=self.casting_director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_view_movies_executive_producer(self):
        res = self.client().get('/movies', headers=self.exec_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    # -----------------------
    # POST '/movies'
    # -----------------------
    def test_add_movie_no_headers(self):
        res = self.client().post('/movies', json = self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Authorization header is expected.")

    def test_add_movies_casting_assistant(self):
        res = self.client().post('/movies', headers=self.casting_assistant_headers, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "the current user has insufficient permissions to perform the requested operation.")

    def test_add_movies_casting_director(self):
        res = self.client().post('/movies', headers=self.casting_director_headers, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "the current user has insufficient permissions to perform the requested operation.")

    def test_add_movies_executive_producer(self):
        res = self.client().post('/movies', headers=self.exec_producer_headers, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    # -----------------------
    # PATCH '/movies'
    # -----------------------
    def test_edit_movie_no_headers(self):
        res = self.client().patch('/movies/1', json = self.edit_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Authorization header is expected.")

    def test_edit_movies_casting_assistant(self):
        res = self.client().patch('/movies/1', headers=self.casting_assistant_headers, json=self.edit_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "the current user has insufficient permissions to perform the requested operation.")

    def test_edit_movies_casting_director(self):
        res = self.client().patch('/movies/2', headers=self.casting_director_headers, json=self.edit_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))
        
    def test_edit_movies_executive_producer(self):
        res = self.client().patch('/movies/2', headers=self.exec_producer_headers, json=self.edit_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    # -----------------------
    # DELETE '/movies'
    # -----------------------
    def test_delete_movie_no_headers(self):
        res = self.client().delete('/movies/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Authorization header is expected.")

    def test_delete_movies_casting_assistant(self):
        res = self.client().delete('/movies/2', headers=self.casting_assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "the current user has insufficient permissions to perform the requested operation.")

    def test_delete_movies_casting_director(self):
        res = self.client().delete('/movies/1', headers=self.casting_director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "the current user has insufficient permissions to perform the requested operation.")

    def test_delete_movies_executive_producer(self):
        res = self.client().delete('/movies/1', headers=self.exec_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], '1')
        self.assertTrue(len(data['movies']))

    '''
    Shows Tests
    '''

    def test_view_shows_no_headers(self):
        res = self.client().get('/shows')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['shows']))


    def test_view_shows_casting_assistant(self):
        res = self.client().get('/shows', headers=self.casting_assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['shows']))

    def test_view_shows_casting_director(self):
        res = self.client().get('/shows', headers=self.casting_director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['shows']))

    def test_view_shows_executive_producer(self):
        res = self.client().get('/shows', headers=self.exec_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['shows']))


    # -----------------------
    # POST '/shows'
    # -----------------------
    def test_add_show_no_headers(self):
        res = self.client().post('/shows', json = self.new_show)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Authorization header is expected.")

    def test_add_shows_casting_assistant(self):
        res = self.client().post('/shows', headers=self.casting_assistant_headers, json=self.new_show)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "the current user has insufficient permissions to perform the requested operation.")

    def test_add_shows_casting_director(self):
        res = self.client().post('/shows', headers=self.casting_director_headers, json=self.new_show)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "the current user has insufficient permissions to perform the requested operation.")

    def test_add_shows_executive_producer(self):
        res = self.client().post('/shows', headers=self.exec_producer_headers, json=self.new_show)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['shows']))


    # -----------------------
    # DELETE '/shows'
    # -----------------------
    def test_delete_show_no_headers(self):
        res = self.client().delete('/shows/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Authorization header is expected.")

    def test_delete_shows_casting_assistant(self):
        res = self.client().delete('/shows/2', headers=self.casting_assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "the current user has insufficient permissions to perform the requested operation.")

    def test_delete_shows_casting_director(self):
        res = self.client().delete('/shows/3', headers=self.casting_director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "the current user has insufficient permissions to perform the requested operation.")

    def test_delete_shows_executive_producer(self):
        res = self.client().delete('/shows/2', headers=self.exec_producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], '2')
        self.assertTrue(len(data['shows']))




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()