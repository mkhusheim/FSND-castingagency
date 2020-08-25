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
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = 'postgresql://mimi:m12345@localhost:5432/castingagency'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # Test Tokens
        self.expired_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ims5Wi0wcHQxa0pmLWFaQm5UU05HQiJ9.eyJpc3MiOiJodHRwczovL21pbXgudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmM2FmMmEwNDc2NjgzMDA2N2VhYTYxYSIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTc3MDMyMTksImV4cCI6MTU5Nzc4OTYxOCwiYXpwIjoiMFBrb1plaTVzWHV6VndHZmJGMk50bDRkN0tKT0pvamUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.O7bwgqs3FNMIv9lFzxqH10PFNXYJQGOCKwoxPjapgbZ-jLlEjvG7GrS3qOdKKjdFeDq0HS8YKBLb5N8IqmN8eb_WLyoowlZTwmRpXMS9d1alnr0FsbkvSxPs52EFu0pMfw4NE7Q4d9XUJhCRslQ1cXQcrq8rIjx4wFHF4wD-y5GryrPl-tqp2yfD3PXcj61YYJNHX-5Dnsp6cgC6hit5E8czQzaf9_QwnYMl0y9HXhNjVAMW2vGoQJ9Q6GUSImvJsActFmDR5ZMPyivf23_EJZ9y_xo-CGTH_2-2jSK1i_llXXHkC4LRHCfcZAsiK6crI2B2VfwEhSSrqDf-FuaP2w'
        self.casting_assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ims5Wi0wcHQxa0pmLWFaQm5UU05HQiJ9.eyJpc3MiOiJodHRwczovL21pbXgudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmM2FmMmEwNDc2NjgzMDA2N2VhYTYxYSIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTgzODY3MzgsImV4cCI6MTU5ODQ3MzEzNywiYXpwIjoiMFBrb1plaTVzWHV6VndHZmJGMk50bDRkN0tKT0pvamUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.lGwwmmksxVWCWrKQR-Pjfxx0CXhBcypGviO_XES7Hocj9duZJLBUFyrIpsUlIIR6eehFhMgEhDVSFQBOWA2sF5ci9eMSY3qgKXf6_Ixr1P441jU8Zfuf1bqqSl9bfFct-MW7VUCnn6TrcZFYeoooJZSlytuyENC2RTmyQ4S1Xe8TPCZx8zYcbCA0WQ_EzLmBvQguOttuZ9k4L9S1IBsoe1bcSV-ms5N41ituJaIh2R88F8uClsRsr-jfjRzmdlqt3D5unB9mPRWubewmYEOMZGBM7rem1bNa0uGw4EOADoDRb5mwwfSD4q8-jRxrSKCPHextW5SfwigeOnklm82Sfw'
        self.casting_director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ims5Wi0wcHQxa0pmLWFaQm5UU05HQiJ9.eyJpc3MiOiJodHRwczovL21pbXgudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMDYzMTg5YTE1YjdiMDAxMzYxZjY1MiIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTgzODY2MTQsImV4cCI6MTU5ODQ3MzAxMywiYXpwIjoiMFBrb1plaTVzWHV6VndHZmJGMk50bDRkN0tKT0pvamUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.keRlkD11BS0V7u-zHylqMEz56pqcsKytTMPN3nEiGaQCxG6AO32bnIQCDJoh8To947zdg1zJ7_ba8MCUDS_hcmp_vGdsuLrzGlyZtjEzcfWhhOKNq55iZ2elaGPASElYlUkCgMYNHOnkmkdE-Xye2HpreLOfOD2leVdQtDNahgb3VzOC0yILkK3KyZqblknRu-BLpr0AdY-bPACkDmin6xi9jBammAiqTgjS_lm45fmoTRXc4zV03SPqMjy8rTHvMGgpdqdOAl739GoTsHgQSx5CL7LA7XB70eOlBOQcnbvYhd3j1ZilTHGxLRJ1ihLFnqEM4kl9DlM5DKa0yBIW4Q'
        self.executive_producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ims5Wi0wcHQxa0pmLWFaQm5UU05HQiJ9.eyJpc3MiOiJodHRwczovL21pbXgudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZWU1MjE5ZWZmNDU2MDAxOTMwNGM2ZiIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTgzODU0MzIsImV4cCI6MTU5ODQ3MTgzMSwiYXpwIjoiMFBrb1plaTVzWHV6VndHZmJGMk50bDRkN0tKT0pvamUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.Stc55qUg2VIHGDKC_IPlVHlvl-5LUHJN33upU5V5L4wST0Y4K5coyy7yf8_Z_Xe95BhbW8PqJetFrpHoIM37r4s1JNYXwrMeeFberOcxrW-j01zeOoMD_SX1Inv5dxO8IkuaYEwVWzQKloLhXpQ6S9_9SAajs7z0xGEK8DPiUkIa-iqDEJoXMXKLTqJCfVTZtK0rnqQDep628E8fA5ry65zC6W5ZPtA3HwtTX2rQcTUH8AOAR00h7XlanKovuMZR63bbXP1XHldsQt9mpisEaS8sqDDNIfXediEP0oj4LUmq0pE7UfMAZm5f3F_pdCRDk2jHn531KzA2o1PSCUzdIA'
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

    # Test get movies, by casting assistant - permitted
    def test_get_movies(self):
        res = self.client().get(
            '/movies', headers={'Authorization': 'Bearer {}'.format(self.casting_assistant_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # Test get actors, by casting assistant - permitted
    def test_get_actors(self):
        res = self.client().get(
            '/actors', headers={'Authorization': 'Bearer {}'.format(self.casting_assistant_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # Test post a new movie, by executive producer - permitted
    def test_post_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers={'Authorization': 'Bearer {}'.format(self.executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # Test post a new actor, by casting director - permitted
    def test_post_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers={'Authorization': 'Bearer {}'.format(self.casting_director_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # Test edit movie, by executive producer - permitted
    def test_edit_movie(self):
        res = self.client().patch('/movies/7', json=self.edit_movie_title,
                                  headers={'Authorization': 'Bearer {}'.format(self.executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movies'], 7)

    # Test edit non-existent movie, by executive producer - permitted
    def test_404_edit_movie(self):
        res = self.client().patch('/movies/1000', json=self.edit_movie_title,
                                  headers={'Authorization': 'Bearer {}'.format(self.executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    # Test edit actor, by executive producer - permitted
    def test_edit_actor(self):
        res = self.client().patch('/actors/17', json=self.edit_actor_age,
                                  headers={'Authorization': 'Bearer {}'.format(self.executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actors'], 17)

    # Test edit a non-existent actor, by executive producer - permitted
    def test_404_edit_actor(self):
        res = self.client().patch('/actors/1000', json=self.edit_actor_age,
                                  headers={'Authorization': 'Bearer {}'.format(self.executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    # Test delete a movie, by executive producer - permitted
    def test_delete_movie(self):
        res = self.client().delete(
            '/movies/6', headers={'Authorization': 'Bearer {}'.format(self.executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movies'], 6)

    # Test delete a non-existent movie, by executive producer - permitted
    def test_delete_movie(self):
        res = self.client().delete(
            '/movies/1000', headers={'Authorization': 'Bearer {}'.format(self.executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    # Test delete a actor, by casting director - permitted
    def test_delete_actor(self):
        res = self.client().delete(
            '/actors/24', headers={'Authorization': 'Bearer {}'.format(self.casting_director_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actors'], 24)

    # Test delete a non-existent actor, by casting director - permitted
    def test_404_delete_actor(self):
        res = self.client().delete(
            '/actors/1000', headers={'Authorization': 'Bearer {}'.format(self.casting_director_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    # Test post a new actor by an unauthorized user, by casting assistant - not permitted
    def test_401_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers={'Authorization': 'Bearer {}'.format(self.casting_assistant_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unauthorized user request")

    # Test post a new actor by an unauthorized user, by casting assistant - not permitted
    def test_401_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers={'Authorization': 'Bearer {}'.format(self.casting_assistant_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unauthorized user request")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
