import os
import sys
from flask import (
    Flask,
    request,
    abort,
    jsonify
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *
from auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # db_drop_and_create_all()
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    # Home page --- Just to check

    @app.route('/')
    def home():
        return jsonify({
            'web': 'Company, Movie and Actors',
            'created by': 'Rahibah Ali'
        })

    # GET: desplay companies and movies
    @app.route('/companies', methods=['GET'])
    def get_companies():
        companies = Company.query.all()
        listCompanies = [Company.format() for Company in companies]

        return jsonify({
            'success': True,
            'companies': listCompanies
        })

    @app.route('/movies', methods=['GET'])
    def get_movies():
        movies = Movie.query.all()
        listMovies = [movie.format() for movie in movies]

        return jsonify({
            'success': True,
            'Movies': listMovies
        })

    # POST: create a new movie
    @app.route('/<company_id>/movies', methods=['POST'])
    @requires_auth('post:movie')
    def create_movies(pay, company_id):
        body = request.get_json()
        title = body.get('title', None)

        try:
            movie = Movie(title=title, owner_id=company_id)
            movie.insert()
            return jsonify({'success': True, 'movie': [movie.format()]})
        except:
            abort(422)

    # PATCH: Update the movie
    @app.route('/<int:company_id>/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(pay, company_id, movie_id):

        M_id = Movie.query.with_entities(Movie.owner_id).filter(Movie.id == movie_id).all()

        if company_id != M_id[0][0]:
            abort(405)

        body = request.get_json()
        title = body.get('title', None)
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        try:
            movie.title = title
            movie.update()
            movie_f = movie.format()

            return jsonify({
                'success': True,
                'movie': movie_f})

        except:
            abort(422)

    # DELETE: delete a specific movie
    @app.route('/<int:company_id>/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(pay, company_id, movie_id):

        M_id = Movie.query.with_entities(Movie.owner_id).filter(Movie.id == movie_id).all()

        if company_id != M_id[0][0]:
            abort(405)

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        try:
            movie.delete()
            return jsonify({
                'success': True,
                'delete': movie_id
            })

        except:
            abort(422)

    # Error Handling
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "bad request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': "unauthorized"
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': "method not allowed"
        }), 405

    @app.errorhandler(406)
    def not_acceptable(error):
        return jsonify({
            'success': False,
            'error': 406,
            'message': "not acceptable"
        }), 406

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "unprocessable"
        }), 422

    # Error handler for AuthError
    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error['description']
        }), error.status_code

    return app


app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
