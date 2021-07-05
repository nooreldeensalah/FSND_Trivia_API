import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

DB_HOST = os.getenv("DB_HOST", "localhost:5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "mypassword")
DB_NAME = os.getenv("DB_NAME", "trivia_test")


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_path = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
        setup_db(self.app, self.database_path)

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
        response = self.client.get("/categories")
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            data["categories"],
            {
                "1": "Science",
                "2": "Art",
                "3": "Geography",
                "4": "History",
                "5": "Entertainment",
                "6": "Sports",
            },
        )

    def test_get_questions(self):
        response = self.client.get("/questions")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data["questions"])
        self.assertGreater(data["total_questions"], 0)

    def test_get_questions_invalid_page(self):
        response = self.client.get("/questions?page=50000")
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "RESOURCE NOT FOUND")

    """
    From the original database
    ----------------------------
    
    trivia_test=# SELECT * FROM questions ORDER BY id;
    -[ RECORD 1 ]-------------------------------------------------------------------------------------------------------------
    id         | 2
    question   | What movie earned Tom Hanks his third straight Oscar nomination, in 1996?
    answer     | Apollo 13
    difficulty | 4
    category   | 5
    ...........
    There is no question with id == 1, (missing)
    There's a question with id == 2.
    deleting behavior will be tested on both.
        """
    # NOTE: THIS TEST WILL ONLY SUCCEED ONCE, YOU HAVE TO RE-POPULATE THE DATABASE IN ORDER TO TEST AGAIN.
    def test_delete_existing_question(self):
        """
        This test will only succeed one time
        """
        response = self.client.delete("/questions/2")

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(Question.query.get(2))

    def test_delete_non_existing_question(self):
        response = self.client.delete("/questions/1")
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "RESOURCE NOT FOUND")

    # NOTE
    def test_adding_non_empty_question(self):
        response = self.client.post(
            "/questions",
            json={
                "question": "New Question",
                "answer": "New Answer",
                "difficulty": "4",
                "category": "3",
            },
        )
        new_question = Question.query.filter(
            Question.question == "New Question"
        ).first()
        # NOTE: I used .first() as the terminal method,
        # instead of .one() or .all() to be able to run the test multiple times

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(new_question)

    def test_adding_question_with_empty_field(self):
        # Testing for any empty field (question, answer, category, difficulty) is done in a similar manner.
        response = self.client.post(
            "/questions",
            json={
                "question": "",
                "answer": "Empty question field",
                "difficulty": "4",
                "category": "3",
            },
        )
        data = response.get_json()
        new_question = Question.query.filter(
            Question.answer == "Empty question field"
        ).first()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["message"], "BAD REQUEST")
        self.assertIsNone(new_question)

    def test_adding_question_with_invalid_endpoint(self):
        response = self.client.post(
            "/questions/2",
            json={
                "question": "New Question",
                "answer": "New Answer",
                "difficulty": "4",
                "category": "3",
            },
        )
        data = response.get_json()
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data["message"], "METHOD NOT ALLOWED")

    def test_search_existing_questions(self):
        # From the the original database.
        """
        ------
        SELECT * FROM questions WHERE question LIKE '%World%';
         id |                               question                               | answer  | difficulty | category
        ----+----------------------------------------------------------------------+---------+------------+----------
         10 | Which is the only team to play in every soccer World Cup tournament? | Brazil  |          3 |        6
         11 | Which country won the first ever soccer World Cup in 1930?           | Uruguay |          4 |        6
        (2 rows)
        --------
        """
        response = self.client.post("/questions", json={"searchTerm": "World"})
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data["questions"])
        self.assertEqual(data["total_questions"], 2)

    def test_search_non_existing_questions(self):
        response = self.client.post("/questions", json={"searchTerm": "ASDSAFLWKQNR"})
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["questions"], [])
        self.assertEqual(data["total_questions"], 0)

    def test_get_questions_by_existing_category(self):
        response = self.client.get("/categories/1/questions")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(data["questions"])
        self.assertGreater(data["total_questions"], 0)
        self.assertEqual(
            data["current_category"], "Science"
        )  # category id 1 corresponds to Science.

    def test_questions_by_non_existing_category(self):
        response = self.client.get(
            "/categories/7/questions"
        )  # There's no category with id = 7.
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "RESOURCE NOT FOUND")

        """
        From the original database
        ---------------------------
        trivia_test=# SELECT * FROM questions WHERE category=1;
         id |                            question                             |      answer       | difficulty | category
        ----+-----------------------------------------------------------------+-------------------+------------+----------
         20 | What is the heaviest organ in the human body?                   | The Liver         |          4 |        1
         21 | Who discovered penicillin?                                      | Alexander Fleming |          3 |        1
         22 | Hematology is a branch of medicine involving the study of what? | Blood             |          4 |        1
        (3 rows)
        ----------------------------
        """

    def test_play_quizzes(self):
        response = self.client.post(
            "/quizzes",
            json={
                "previous_questions": [],
                "quiz_category": {"type": "Science", "id": "1"},
            },
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["previous_questions"]), 1)
        self.assertIsNotNone(data["question"])

    def test_play_quizzes_with_one_previous_question(self):
        response = self.client.post(
            "/quizzes",
            json={
                "previous_questions": [20],
                "quiz_category": {"type": "Science", "id": "1"},
            },
        )
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["previous_questions"]), 2)
        self.assertIsNotNone(data["question"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
