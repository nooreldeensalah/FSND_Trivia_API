import json
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
    CORS(app)  # Default config, CORS enabled on all routes, origins, methods.

    # Request CORS Headers
    @app.after_request
    def after_request(response):
        """

        Args:
            response:

        Returns:
            response after adding Access Control.

        """
        allowed_headers = "Content-Type,Authorization,true"
        response.headers.add("Access-Control-Allow-Headers", allowed_headers)
        allowed_methods = "GET,PUT,POST,DELETE,OPTIONS"
        response.headers.add("Access-Control-Allow-Methods", allowed_methods)
        return response

    def paginate_questions(selection):
        """

        Args:
            selection:

        Returns:
            A list of 10 questions formatted in JSON form.

        """
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        formatted_questions = [question.format() for question in selection]
        paginated_questions = formatted_questions[start:end]
        return paginated_questions

    @app.route("/categories")
    def get_categories():
        """
        GET request to retrieve a list of all categories.
        Returns: A list of all categories in {"id": "type} format.

        """
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = {
            f"{category.id}": f"{category.type}" for category in categories
        }

        return jsonify({"categories": formatted_categories})

    @app.route("/questions")
    def get_questions():
        """
        GET request to retrieve list of all questions.
        Returns: A json response with the following contents:
        - A list of 10 questions.
        - The total number of questions.
        - The categories available.
        - The current category (default = None).

        """
        questions = Question.query.order_by(Question.id).all()
        paginated_questions = paginate_questions(questions)
        if len(paginated_questions) == 0:
            abort(404)

        return jsonify(
            {
                "questions": paginated_questions,
                "total_questions": len(questions),
                "categories": get_categories().json["categories"],
                "current_category": None,  # According to a mentor in https://knowledge.udacity.com/questions/82424.
            }
        )

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        """
        DELETE request to delete a question by id.
        Args:
            question_id: The id of the question to be deleted.

        Returns:
            flask.Response object with status code = 200.
        """
        try:
            question = Question.query.get(question_id)
            question.delete() if question is not None else abort(404)
            return flask.Response(status=200)
        except BaseException:
            abort(422)

    @app.route("/questions", methods=["POST"])
    def add_question_or_search():
        """
        POST request to add new question.
        Also implements search functionality by question's string.
        Returns:
            Adding new question:
                json.dumps({"success": True}), 201, {"ContentType": "application/json"})
            Searching: A json response body with the following contents:
                - A list of 10 (maximum) matching questions.
                - Total number of matching questions.
                - current_category (default = None).

        """
        request_body = request.get_json()
        try:
            if search_term := request_body.get("searchTerm", None):
                matching_questions = (
                    Question.query.order_by(Question.id)
                    .filter(Question.question.ilike(f"%{search_term}%"))
                    .all()
                )
                paginated_questions = paginate_questions(matching_questions)
                return jsonify(
                    {
                        "questions": paginated_questions
                        if len(matching_questions)
                        else [],
                        "total_questions": len(matching_questions),
                        "current_category": None,
                    }
                )
            else:
                question = Question(**request_body)
                question.insert()
                return (
                    json.dumps({"success": True}),
                    201,
                    {"ContentType": "application/json"},
                )

        except BaseException:
            abort(422)

    @app.route("/categories/<int:category_id>/questions")
    def get_questions_by_category(category_id):
        """
        GET request to retrieve list of all questions by category.
        Returns: A json response with the following contents:
        - A list of 10 questions (maximum) from the chosen category..
        - The total number of questions matching the category.
        - The current category (default = None).
        """
        questions = (
            Question.query.order_by(Question.id)
            .filter(Question.category == category_id)
            .all()
        )
        paginated_questions = paginate_questions(questions)
        if len(paginated_questions) == 0:
            abort(404)
        return jsonify(
            {
                "questions": paginated_questions,
                "total_questions": len(questions),
                "current_category": Category.query.get(category_id).type,
            }
        )

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
