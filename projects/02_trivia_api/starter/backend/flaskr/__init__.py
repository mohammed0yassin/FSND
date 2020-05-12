import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request,selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [question.format() for question in selection]
  current_questions = questions[start:end]
  
  return current_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  
  '''
  @DONE TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"*": {"origins": "*"}})
  '''
  @DONE TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
  '''
  @DONE TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    selection = Category.query.all()
    categories = {category.id:category.type for category in selection} 

    return jsonify({
      'success': True,
      'categories': categories
    })


  '''
  @DONE TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions/')
  def get_questions():
    selection = Question.query.all()
    current_questions = paginate_questions(request,selection)
    if len(current_questions) == 0:
      abort(404)

    cat_selection = Category.query.all()
    categories = {category.id:category.type for category in cat_selection} 
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions':len(selection),
      'categories': categories,
      'current_category': None
    })
  '''
  @DONE TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)
      
      question.delete()

      selection = Question.query.all()
      current_questions = paginate_questions(request,selection)
    
      cat_selection = Category.query.all()
      categories = {category.id:category.type for category in cat_selection} 
      return jsonify({
        'success': True,
        'deleted': question_id,
        'questions': current_questions,
        'total_questions':len(selection),
        'categories': categories,
        'current_category': None
      })
    
    except:
      abort(422)



  '''
  @DONE TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions', methods=['POST'])
  def create_question():
    
    try:
      # Search for questions
      search = request.get_json().get('searchTerm', None)
      if search:
        selection = Question.query.filter(Question.question.ilike('%{}%'.format(search))).all()
        current_questions = paginate_questions(request,selection)

        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(selection),
          'current_category': None,
        })

      # Create a new question

      data = {
        'question': request.get_json()['question'],
        'answer': request.get_json()['answer'],
        'category': request.get_json()['category'],
        'difficulty': request.get_json()['difficulty']
      }

      if not data['question'] or not data['answer']: #if no question or answer are entered. 
        abort(404)    #it doesn't work after sumbitting a question succeffult for thefirst time because of a fault in the frontend 
       #                            which doesn't clear the variable of the field unless refreshed the page
       #                             ,hense sends the last created question with the request even if you cleared the field.
      
      question = Question(**data)
      question.insert()
      return jsonify({
        'success': True,
        'created': question.id
      })
    
    except:
      abort(422)

  '''
  @DONE TODO: ^ in create_question()
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @DONE TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def select_category(category_id):
    selection = Question.query.filter(Question.category == category_id).all()
    current_questions = paginate_questions(request,selection)
    
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(selection),
      'current_category': category_id
    })
    


  '''
  @DONE TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_game():
    try:
      body = request.get_json()
      current_category = request.get_json()['quiz_category']['id']
      previous_questions = request.get_json()['previous_questions']
      
      if current_category == 0:
        questions_ids = Question.query.with_entities(Question.id).all()
      else:
        questions_ids = Question.query.filter(Question.category == current_category).with_entities(Question.id).all()
      
      available_ids = [value for value, in questions_ids] # getting the list of availabe ids in questions table 
      
      if set(available_ids) == set(previous_questions):
        return jsonify({
          'success': True,
          'question': False
        })  
      
      else:
        random_id = random.choice([i for i in available_ids if i not in previous_questions])
        current_question = Question.query.get(random_id).format()

        return jsonify({
          'success': True,
          'previousQuestions': previous_questions,
          'question': current_question

        })

    except:
      abort(422)
  '''
  @DONE TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
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
  
  return app

  