# CapstoneProject_FSND


## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.



## API Endpoint
GET ```/companies ```
- View all companies
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```
GET ```/movies ```
- Return movies 


DELETE ```/${id}/movies/${id} ```
- Delete a specified movie by using the ID.

PATCH ```/${id}/movies/${id} ```
- Update a specified movie by using the ID.

POST ```/${id}/movies ```
- Create a new movie.

**Error Handling**

The endpoint handles seven errors:
- 400: Bad Request
- 401: Unauthorized
- 404: Resource Not Found
- 405: Method Not Alowed
- 406: Not acceptable
- 422: Not Processable
- 500: Server error

Example:
```
{
   'success': False,
   'error': 404,
    'message': "resource not found"
    }
 ```


## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:companies`
   - `get:movies`
   - `post:movie`
   - `patch:movie`
   - `delete:movie`
6. Create new roles for:
   - Visitor
     - can `get:movies` and `get:companies`
   - Director
     - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com).
   - Register 2 users - assign the Visitor role to one and Director role to the other.
   - Sign into each account and make note of the JWT.
   - Import the postman collection `./movie-Actors.postman_collection.json`
   - Right-clicking the collection folder for Visitor and Director, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
   - Run the collection and correct any errors.
   - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

## Testing
To run the tests, run
```
dropdb moviesactors_test
createdb moviesactors_test
python test.py
```

## Deblay on Heroku
Link: https://movie-actors.herokuapp.com/

