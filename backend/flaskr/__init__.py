import random
import flask
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # Create and configure the app
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
        question = Question.query.get(question_id)
        question.delete() if question is not None else abort(404)
        return flask.Response(status=200)

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
        if (search_term := request_body.get("searchTerm", None)) is not None:
            # If the search_term is empty, it will retrieve all questions.
            matching_questions = (
                Question.query.order_by(Question.id)
                .filter(Question.question.ilike(f"%{search_term}%"))
                .all()
            )
            paginated_questions = paginate_questions(matching_questions)
            return jsonify(
                {
                    "questions": paginated_questions if len(matching_questions) else [],
                    "total_questions": len(matching_questions),
                    "current_category": None,
                }
            )
        else:
            # Checks if both question and answer fields are empty.
            if not request_body["question"] or not request_body["answer"]:
                abort(400)
            try:
                # Try adding the question to the database.
                question = Question(**request_body)
                question.insert()
                return jsonify({"success": True}), 201
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

    @app.route("/quizzes", methods=["POST"])
    def play():
        """
        POST request to play the trivia game.
        Returns:
            - A random question from a chosen category, or from all categories.
            - A list of previous questions ids, to ensure to repetition.
        """
        request_payload = request.get_json()
        category = request_payload["quiz_category"]
        previous_questions = request_payload["previous_questions"]
        if category["id"] == 0:  # From all categories.
            while True:
                # FIXME: Ensures no repeated questions, but the application freezes when the questions end.
                random_question = random.choice(Question.query.all())
                if random_question.id not in previous_questions:
                    break
        else:
            while True:
                # FIXME: Ensures no repeated questions, but the application freezes when the questions end.
                random_question = random.choice(
                    Question.query.filter(Question.category == category["id"]).all()
                )
                if random_question.id not in previous_questions:
                    break
        previous_questions.append(random_question.id)
        return jsonify(
            {
                "question": random_question.format(),
                "previous_questions": previous_questions,
            }
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": 400, "message": "BAD REQUEST"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": 404, "message": "RESOURCE NOT FOUND"}), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({"error": 405, "message": "METHOD NOT ALLOWED"}), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"error": 422, "message": "UNPROCESSABLE ENTITY"}), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"error": 500, "message": "SERVER ERROR"}), 500

    return app
