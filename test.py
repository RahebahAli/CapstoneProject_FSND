import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db_drop_and_create_all, Movie

DIRECTOR_TOKEN = os.getenv('DIRECTOR')
VISITOR_TOKEN = os.getenv('VISITOR')


class MovieTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "moviesactors_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432',
                                                        self.database_name
                                                        )

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            db_drop_and_create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # GET: test the display company
    def test_get_companies(self):
        res = self.client().get('/companies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['companies'])

    # GET: test the display movie
    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # POST: test add new movie
    def test_correct_add_new_movie(self):
        n_data = {"title": "Titanic"}
        res = self.client().post("1/movies",
            headers={'Authorization': 'Bearer ' + DIRECTOR_TOKEN},
            json=n_data)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_not_allowed_add_new_movie(self):
        n_data = {"title": "Titanic"}
        res = self.client().post("/movies",
            headers={'Authorization': 'Bearer ' + VISITOR_TOKEN},
            json=n_data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # PATCH: test a update the movie
    def test_correct_update_movie(self):
        n_data = {"title": "The Shawshink Redemption"}
        res = self.client().patch('1/movies/1',
            json=n_data,
            headers={'Authorization': 'Bearer ' + DIRECTOR_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_unprocessable_update_movie(self):
        n_data = {"title": 100}
        res = self.client().patch('1/movies/1',
            json=n_data,
            headers={'Authorization': 'Bearer ' + VISITOR_TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'unprocessable')

    # DELETE: test a delete the movie
    def test_delete_movie(self):
        res = self.client().delete('1/movies/1',
            headers={'Authorization': 'Bearer ' + DIRECTOR_TOKEN})
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(movie, None)

    def test_404_if_movie_does_not_exist(self):
        res = self.client().delete('/questions/1000',
            headers={'Authorization': 'Bearer ' + VISITOR_TOKEN})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
