import os
from flask import Flask, render_template, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import exc
from auth import AuthError, requires_auth
from models import  setup_db, Movie, Actor


def create_app(test_config=None):
    
    app = Flask(__name__)
   
    setup_db(app)
    CORS(app)
    CORS(app, resources={"/": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, PUT, POST,DELETE, OPTIONS')
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response    

    # Home
    @app.route('/')
    def index():
        return render_template('index.html')

    
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies') 
    def get_movies(payload):
        try:
            movies = Movie.query.all()
            if len(movies) == 0:
                abort(404) 
            return jsonify({
                'success': True,
                'movies': [movie.format() for movie in movies]
                }), 200
        except Exception as e:
            print(e)            

    #  {   "id":2, 
    #   "title":"test1",
    #   "release_date":"2023-03-03"                                                                                                       
    #  }
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
        movie_data = request.get_json()
        try:
            movie = Movie(
            title=movie_data['title'],
            id=movie_data['id'],
            release_date=movie_data['release_date']
            )
            if movie.title == '' or movie.release_date == '':
             abort(422)

            try:
             movie.insert()
             return jsonify({
                'success': True,
                'movie': movie.format()
                }), 200
            except Exception:
             abort(500)
        except:
             abort(422)

       

    @app.route('/movies/<int:id>', methods=['GET', 'PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, id):
        get_movie = request.get_json()
        movie = Movie.query.filter(Movie.id == id).first()
        if movie:
            movie.title = get_movie['title'] 
            movie.release_date = get_movie['release_date'] 
        else:
            abort(404)
        try:
            movie.update()

            return jsonify({
                'success': True,
                'movie': [movie.format()]
                }), 200
        except Exception:
            abort(500)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):
        movie = Movie.query.filter(Movie.id == id).first()
        if movie:
            try:
                movie.delete()
                return jsonify({
                    'success': True,
                    'delete': id
                    }), 200
            except Exception:
                abort(500)
        else:
            abort(404)

    # Actor endpoints
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            actors = Actor.query.all()
            if len(actors) == 0:
                abort(404) 
            return jsonify({
                            'success': True,
                            'actors': [actor.format() for actor in actors]
                            }), 200
        except Exception as e:
            print(e)
            abort(500)

    # {"age": 23,"gender": "F",  "name": "test","id":2  }

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(payload):
        movie_data = request.get_json()
        try:
            actor = Actor(
            name=movie_data['name'],
            age=movie_data['age'],
            gender=movie_data['gender'],
             id=movie_data['id']
            )
            if actor.name == '' or actor.age == '' or actor.gender == '':
             abort(422)
            
            try:
             actor.insert()

             return jsonify({
                'success': True,
                'actor': actor.format()
                }), 200
            except Exception as e:
             print(e)
             abort(500)
        except:
             abort(422)       
       

    @app.route('/actors/<int:id>', methods=['GET', 'PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, id):
        data = request.get_json()
        actor = Actor.query.filter(Actor.id == id).first()
        if actor:
            actor.name = data['name'] 
            actor.age = data['age'] 
            actor.gender = data['gender'] 
            try:
                actor.update()
                return jsonify({
                    'success': True,
                    'actor': [actor.format()]
                    }), 200
            except Exception:
                abort(500)
        else:
            abort(404)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        actor = Actor.query.filter(Actor.id == id).first()
        if actor:
            try:
                actor.delete()
                return jsonify({
                    'success': True,
                    'delete': id
                    }), 200
            except Exception:
                abort(500)
        else:
            abort(404)

    # Error Handling
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request, please check your inputs"
            }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found."
            }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
            }), 500

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable. Check your input.'
          }), 422

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "You are not allowed to access this resource",
                }), 403

    @app.errorhandler(AuthError)
    def auth_error(ex):
        res = jsonify(ex.error)
        res.status_code = ex.status_code
        return res
    
    return app