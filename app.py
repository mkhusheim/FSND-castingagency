import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, setup_db, Movies, Actors
import json
from auth.auth import AuthError, requires_auth
import datetime


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # Endpoints
    @app.route('/')
    def get_greeting():
        #excited = os.environ['EXCITED']
        greeting = "Hello"
        return greeting

    # Get movies endpoint
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(token):
        movies = Movies.query.order_by('id').all()
        formatted_movies = []
        for movie in movies:
            formatted_movies.append({
                "id": movie.id,
                "title": movie.title,
                "release_date": movie.release_date})
        # formatted_movies = json.dumps(movies)
        return jsonify({
            "success": True,
            "movies": formatted_movies
        })

    # Get actors endpoint
    @ app.route('/actors')
    @ requires_auth('get:actors')
    def get_actors(token):
        actors = Actors.query.all()
        formatted_actors = []
        for actor in actors:
            formatted_actors.append({
                "id": actor.id,
                "name": actor.name,
                "age": actor.age,
                "gender": actor.gender})
        return jsonify({
            "success": True,
            "actors": formatted_actors
        })

    # post movie endpoint
    @ app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def add_movie(token):
        body = json.loads(request.data, strict=False)
        title = body.get('title', None)
        release_date = body.get('release_date', None)
        #release_date = datetime.datetime.strptime(release_date_str, '%Y-%m-%d ')
        # print(release_date.date())
        try:
            new_movie = Movies(title=title, release_date=date)
            # new_movie.insert()
            db.session.add(new_movie)
            db.session.commit()
            return jsonify({
                "success": True,
                "movies": new_movie.name
            })
        except:
            db.session.rollback()
            abort(422)

    # post actor endpoint
    @ app.route('/actors', methods=['POST'])
    @ requires_auth('post:actor')
    def add_actor(token):
        body = json.loads(request.data, strict=False)
        id = body.get('id', None)
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        try:
            new_actor = Actors(name=name, age=age, gender=gender)
            db.session.add(new_actor)
            db.session.commit()
            return jsonify({
                "success": True,
                "actors": new_actor.name
            })
        except:
            db.session.rollback()
            abort(422)

    # edit movie endpoint
    @app.route('/movies/<int:movieID>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def edit_movie(token, movieID):
        selected_movie = Movies.query.filter(Movies.id == movieID).one_or_none()
        if selected_movie is None:
            abort(404)
        try:
            body = json.loads(request.data, strict=False)
            title = body.get('title', None)
            release_date = body.get('release_date', None)

            if title != None:
                selected_movie.title = title
            if release_date != None:
                selected_movie.release_date = release_date
            db.session.update(selected_movie)
            db.session.commit()

            return jsonify({
                "success": True,
                "actors": movieID
            })
        except:
            db.session.rollback()
            abort(422)

    # edit actor endpoint
    @ app.route('/actors/<int:actorID>', methods=['PATCH'])
    @ requires_auth('patch:actor')
    def edit_actor(token, actorID):
        selected_actor = Actors.query.filter(Actors.id == actorID).one_or_none()
        if selected_actor is None:
            abort(404)
        try:
            body = json.loads(request.data, strict=False)
            name = body.get('name', None)
            age = body.get('age', None)
            gender = body.get('gender', None)

            if name != None:
                selected_actor.name = name
            if age != None:
                selected_actor.age = age
            if gender != None:
                selected_actor.gender = gender

            db.session.update(selected_actor)
            db.session.commit()

            return jsonify({
                "success": True,
                "actors": actorID
            })
        except:
            db.session.rollback()
            abort(422)

    # delete movie endpoint
    @ app.route('/movies/<int:movieID>', methods=['DELETE'])
    @ requires_auth('delete:movie')
    def delete_movie(token, movieID):
        selected_movie = Movies.query.filter(Movies.id == movieID).one_or_none()
        if selected_movie is None:
            abort(404)
        try:
            # selected_movie.delete()
            db.session.delete(selected_movie)
            db.session.commit()
        except:
            abort(422)
            db.session.rollback()
        return jsonify({
            "success": True,
            "movies": movieID
        })

    # edit movie endpoint
    @ app.route('/actors/<int:actorID>', methods=['DELETE'])
    @ requires_auth('delete:actor')
    def delete_actor(token, actorID):
        selected_actor = Actors.query.filter(Actors.id == actorID).one_or_none()
        if selected_actor is None:
            abort(404)
        try:
            # selected_actor.delete()
            db.session.delete(selected_actor)
            db.session.commit()
        except:
            db.session.rollback()
            abort(422)
        return jsonify({
            "success": True,
            "actors": actorID
        })

    # Error Handling
    '''
    Error handling for unprocessable entity
    '''

    @ app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    '''
    Error handling for not found entity
    '''

    @ app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    '''
    Error handling for not allowed method
    '''

    @ app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    '''
    Error handling for unauthorized requests
    '''

    @ app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized user request"
        }), 401

    '''
    Error handling for forbidden requests
    '''

    @ app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "forbidden request"
        }), 403

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080)
