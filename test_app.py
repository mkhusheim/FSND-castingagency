import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import db, setup_db, Movies, Actors


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the Casting Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "castingagency"
        self.database_path = 'postgresql: // mimi
        : m12345@localhost: 5432/castingagency'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # Test Data
        self.new_actor = ({
            "name": "Morgan Freeman",
            "age": 82,
            "gender": "male"
        })
        self.new_movie = ({
            "title": "Addams Family",
            "release_date": "2019-10-6 00:00:00 GMT"
        })
        self.edit_movie_title = ({
            "title": "Cindrella"
        })
        self.edit_actor_age = ({
            "age": 24
        })

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test get movies,
    # by casting assistant - permitted
    def test_get_movies(self):
        res = self.client().get(
            '/movies', headers={'Authorization': 'Bearer {}'
                                .format(self.casting_assistant_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # Test get actors,
    # by casting assistant - permitted
    def test_get_actors(self):
        res = self.client().get(
            '/actors', headers={'Authorization': 'Bearer {}'
                                .format(self.casting_assistant_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # Test post a new movie,
    # by executive producer - permitted
    def test_post_new_movie(self):
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers={'Authorization': 'Bearer {}'
                                          .format
                                          (self.executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # Test post a new actor,
    # by casting director - permitted
    def test_post_new_actor(self):
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers={'Authorization': 'Bearer {}'
                                          .format
                                          (self.casting_director_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # Test edit movie,
    # by executive producer - permitted
    def test_edit_movie(self):
        res = self.client().patch('/movies/7',
                                  json=self.edit_movie_title,
                                  headers={'Authorization': 'Bearer {}'
                                           .format
                                           (self.executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movies'], 7)

    # Test edit non-existent movie,
    # by executive producer - permitted
    def test_404_edit_movie(self):
        res = self.client().patch('/movies/1000',
                                  json=self.edit_movie_title,
                                  headers={'Authorization': 'Bearer {}'
                                           .format
                                           (self.executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    # Test edit actor,
    # by executive producer - permitted
    def test_edit_actor(self):
        res = self.client().patch('/actors/17',
                                  json=self.edit_actor_age,
                                  headers={'Authorization': 'Bearer {}'
                                           .format
                                           (self.executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actors'], 17)

    # Test edit a non-existent actor,
    # by executive producer - permitted
    def test_404_edit_actor(self):
        res = self.client().patch('/actors/1000',
                                  json=self.edit_actor_age,
                                  headers={'Authorization': 'Bearer {}'
                                           .format
                                           (self.executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    # Test delete a movie,
    # by executive producer - permitted
    def test_delete_movie(self):
        res = self.client().delete(
            '/movies/6', headers={'Authorization': 'Bearer {}'
                                  .format
                                  (self.executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movies'], 6)

    # Test delete a non-existent movie,
    # by executive producer - permitted
    def test_delete_movie(self):
        res = self.client().delete(
            '/movies/1000', headers={'Authorization': 'Bearer {}'
                                     .format
                                     (self.executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    # Test delete a actor,
    # by casting director - permitted
    def test_delete_actor(self):
        res = self.client().delete(
            '/actors/24', headers={'Authorization': 'Bearer {}'
                                   .format
                                   (self.casting_director_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actors'], 24)

    # Test delete a non-existent actor,
    # by casting director - permitted
    def test_404_delete_actor(self):
        res = self.client().delete(
            '/actors/1000', headers={'Authorization': 'Bearer {}'
                                     .format
                                     (self.casting_director_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    # Test post a new actor by an unauthorized user,
    # by casting assistant - not permitted
    def test_401_new_actor(self):
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers={'Authorization': 'Bearer {}'
                                          .format
                                          (self.casting_assistant_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unauthorized user request")

    # Test post a new actor by an unauthorized user,
    # by casting assistant - not permitted

    def test_401_new_actor(self):
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers={'Authorization': 'Bearer {}'
                                          .format
                                          (self.casting_assistant_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unauthorized user request")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
