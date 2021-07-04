import os

import flask
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(
        app, resources={r"*": {"origins": "*"}}
    )  # Default config, CORS enabled on all routes, origins, methods.

    # CORS Headers
    @app.after_request
    def after_request(response):
        allowed_headers = "Content-Type,Authorization,true"
        response.headers.add("Access-Control-Allow-Headers", allowed_headers)
        allowed_methods = "GET,PUT,POST,DELETE,OPTIONS"
        response.headers.add("Access-Control-Allow-Methods", allowed_methods)
        return response

    def paginate_questions(selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = [question.format() for question in selection]
        current_questions = questions[start:end]
        return current_questions

    @app.route("/categories")
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = {
            f"{category.id}": f"{category.type}" for category in categories
        }

        return jsonify({"categories": formatted_categories})

    @app.route("/questions")
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(questions)
        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "questions": current_questions,
                "total_questions": len(questions),
                "categories": get_categories().json["categories"],
                "current_category": None,  # According to a mentor in https://knowledge.udacity.com/questions/82424.
            }
        )

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete() if question is not None else abort(404)
            return flask.Response(status=200)
        except BaseException:
            abort(422)

    """
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  """

    """
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  """

    """
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  """

    """
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  """

    """
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  """

    return app
