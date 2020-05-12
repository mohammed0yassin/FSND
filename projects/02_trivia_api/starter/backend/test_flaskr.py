import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres','12345678','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Test_Flaskr Question',
            'answer': 'Test_Ans',
            'category': '1',
            'difficulty': '4'
        }

        self.new_empty_question = {
            'question': '',
            'answer': '',
            'category': '1',
            'difficulty': '4'
        }

        self.new_game = {
            "previous_questions": [10, 15], 
            "quiz_category": {"type": "Art", "id": "2"}
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len((data['categories'])))

    def test_get_questions(self):
        res = self.client().get('/questions/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len((data['categories'])))

    def test_404_sent_request_beyond_valid_page(self):
        res = self.client().get('/questions/?page=999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')
        
    # Will only work when id = 2 exists in questions table
    def test_delete_questions(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)  

        self.assertEqual(data['success'],True)
        self.assertEqual(data['deleted'],2)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len((data['categories'])))


    def test_create_question(self):
        res = self.client().post('/questions', json = self.new_question)
        data = json.loads(res.data) 

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_422_create_question_with_empty_question_answer_fields(self):
        res = self.client().post('/questions', json = self.new_empty_question)
        data = json.loads(res.data) 
       
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unproccessable')      

    def test_get_questions_search_with_results(self):
        res = self.client().post('/questions', json = {"searchTerm": "a"})
        data = json.loads(res.data)# "a" is a common letter and it will probably be at least in 1 question

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_select_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue((data['current_category']), 1)
 
    
    def test_play_game(self):
        res = self.client().post('/quizzes', json = self.new_game)
        data = json.loads(res.data) 

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['previousQuestions'], self.new_game['previous_questions'])
        self.assertTrue(data['question'])
       
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()