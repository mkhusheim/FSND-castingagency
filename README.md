# Full Stack Nanodegree Capstone Project - Casting Agency

This is the final project for Udacity Full Stack Nanodegree to apply all the knowledge learned throughout the course. The application is for a a Casting Agency, a company that creates movies and manages assigning actors to those movies.


## Getting Started

### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

### Installing Requirements
To Install all requirements run the following command in your terminal:

```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.

### Running Locally:

1. Setup database URL:

```bash
export DATABASE_URL="{YOUR_DATABASE_URL_HERE}"
```

2. Run local migrations using manage.py file:

```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

3. Run the application using the command:

```bash
python app.py
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## API Reference

### Getting Started

- Base URL: At present this app only be run locally and is not hosted as a base URL. The backend app is hosted at the default, 'http://0.0.0.0:5000'.
- Authentication: Auth0 Authentication, requires signup and login through https://mimx.us.auth0.com/authorize?audience=castingagency&response_type=token&client_id=0PkoZei5sXuzVwGfbF2Ntl4d7KJOJoje&redirect_uri=https://0.0.0.0:8080/login

### Endpoints

#### GET /movies
- General:
-- Returns a list of movies
-- Requires permission (get:movies)
- Sample:
```
{
    "movies": [{
            "id": 1,
            "title": Finding Nemo,
            "release_date": "2003-10-10 00:00:00",
        },
        {
            "id": 2,
            "title": The Addams Family,
            "release_date": "2019-19-25 00:00:00",
        }
        {
            "id": 3,
            "title": Toy Story,
            "release_date": "1995-03-22 00:00:00",
        }],
    "success": true
}
```

#### GET /actors
- General:
-- Returns a list of actors
-- Requires permission (get:actors)
- Sample:
```
{
    "actors": [
        {
            "age": 64,
            "gender": "male",
            "id": 1,
            "name": "Tom Hanks"
        },
        {
            "age": 67,
            "gender": "male",
            "id": 2,
            "name": "Tim Allen"
        },
        {
            "age": 73,
            "gender": "male",
            "id": 3,
            "name": "Albert Brooks"
        },
        {
            "age": 41,
            "gender": "male",
            "id": 4,
            "name": "Oscar Isaac"
        }
    ],
    "success": true
}
```

#### POST /movies
- General:
-- Add a movie
-- Requires permission (post:movie)
-- Returns movie name
- Sample:
```
{
    "movies": "Ratatouille",
    "success": true
}
```

#### POST /actors
- General:
-- Add an actor
-- Requires permission (post:actor)
-- Returns actor name
- Sample:
```
{
    "actors": "Patton Oswalt",
    "success": true
}
```

#### PATCH /movies/2
- General:
-- Edit a movie
-- Requires permission (patch:movie)
-- Returns movie id
- Sample:
```
{
    "movies": 2,
    "success": true
}
```

#### PATCH /actors/2
- General:
-- Edit an actor
-- Requires permission (patch:actor)
-- Returns actor id
- Sample:
```
{
    "actors": 2,
    "success": true
}
```

#### DELETE /movies/1
- General:
-- Delete a movie
-- Requires permission (delete:movie)
-- Returns movie id
- Sample:
```
{
    "movies": 1,
    "success": true
}
```
#### DELETE /actors/1
- General:
-- Delete an actor
-- Requires permission (delete:actor)
-- Returns actor id
- Sample:
```
{
    "actors": 1,
    "success": true
}
```
### Error Handling

Errors are returned as JSON objects in the following format:
```
{
   "success": False,
   "error": 400,
   "message" "bad request"
}
```
The API will return four error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 405: Method not allowed

## Testing
To run the tests, run
```
python test_app.py
```
