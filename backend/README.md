# Backend - Full Stack Trivia API 

----------------

### API Documentation



#### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

#### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "error": 400,
    "message": "BAD REQUEST"
}
```
The API will return four error types when requests fail:
- 400: Bad Request.
- 404: Resource Not Found.
- 405: Method Not Allowed.
- 422: Unprocessable Entity.

### Endpoints
- GET '/categories'
- GET '/questions'
- GET 'categories/<category_id>/questions'
- DELETE '/questions/<question_id>'
- POST '/questions'
- POST '/quizzes'

#### GET '/categories'

- Retrieves a dictionary object of all categories.
- Request Arguments: None
- Returns: A dictionary of categories in {"id": "type} format.
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```
#### GET 'questions'
- Retrieves a list of questions paginated in groups of 10.
- Request Arguments: None.
  ```
  curl localhost:5000/questions?page=1
  ```
- Returns: A json object with the following contents:
    - A list of questions (10 maximum).
    - The total number of questions.
    - Categories dictionary in id:type format.
    - The current category (default = None).
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "total_questions": 20
}
```
#### GET 'categories/<category_id>/questions'
- Retrieves a list of questions according to a specific category.
- Request Arguments: None.
- Returns: A json object with the following contents:
    - A list of questions (up to 10) from the chosen category.
    - The total number of questions in the chosen category.
    - The current category.
```
{
  "current_category": "Entertainment", 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "total_questions": 2
}
```
#### DELETE '/questions/<question_id>'
- Deletes a question if it exists in the database.
- Request Arguments: None.
- Returns: None.

#### POST '/questions'

- POST method to submit new questions and to search for questions.

-------
**INSERTING QUESTIONS**:

- Request Arguments: Question's data (question, answer, category, difficulty)
        
``` 
{"question":"New Question","answer":"New Answer","difficulty":1,"category":1}
 ```

- Returns: a JSON object with a string to indicate success.

```
{"success": true}
```

------------
**SEARCHING**

- Request Arguments: Search term.
```
{"SearchTerm": "World"} 
```

- Returns: A json response body with the following contents:
  
    - A list of 10 (maximum) matching questions.
    - Total number of matching questions.
    - current_category (default = None).
``` 
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ], 
  "total_questions": 2
}
```

#### POST 'quizzes'

- POST request used to play the trivia game.
- Request Arguments: 
    - A list of previously encountered questions ids.
    - A category object; containing the type of the category and it's id. (id = 0 corresponds to all categories.)
```    
{"previous_questions":[],"quiz_category":{"type":"Science","id":"1"}}
```
- Returns:
    - A random question from a chosen category, or from all categories.
    - A list of previously encountered questions ids.
```
{
  "previous_questions": [
    30
  ], 
  "question": {
    "answer": "TEsts", 
    "category": 1, 
    "difficulty": 1, 
    "id": 30, 
    "question": "Teest"
  }
}
```
--------------------------
### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the root directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

--------

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

--------------

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

--------------

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 


----------

## Review Comment to the Students
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/api/v1.0/categories'
GET ...
POST ...
DELETE ...

GET '/api/v1.0/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

--------
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
