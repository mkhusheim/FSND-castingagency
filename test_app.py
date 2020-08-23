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

        # Tokens
        self.expired_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ims5Wi0wcHQxa0pmLWFaQm5UU05HQiJ9.eyJpc3MiOiJodHRwczovL21pbXgudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmM2FmMmEwNDc2NjgzMDA2N2VhYTYxYSIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTc3MDMyMTksImV4cCI6MTU5Nzc4OTYxOCwiYXpwIjoiMFBrb1plaTVzWHV6VndHZmJGMk50bDRkN0tKT0pvamUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.O7bwgqs3FNMIv9lFzxqH10PFNXYJQGOCKwoxPjapgbZ-jLlEjvG7GrS3qOdKKjdFeDq0HS8YKBLb5N8IqmN8eb_WLyoowlZTwmRpXMS9d1alnr0FsbkvSxPs52EFu0pMfw4NE7Q4d9XUJhCRslQ1cXQcrq8rIjx4wFHF4wD-y5GryrPl-tqp2yfD3PXcj61YYJNHX-5Dnsp6cgC6hit5E8czQzaf9_QwnYMl0y9HXhNjVAMW2vGoQJ9Q6GUSImvJsActFmDR5ZMPyivf23_EJZ9y_xo-CGTH_2-2jSK1i_llXXHkC4LRHCfcZAsiK6crI2B2VfwEhSSrqDf-FuaP2w'
        self.casting_assistant_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ims5Wi0wcHQxa0pmLWFaQm5UU05HQiJ9.eyJpc3MiOiJodHRwczovL21pbXgudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmM2FmMmEwNDc2NjgzMDA2N2VhYTYxYSIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTc5NTM4MzAsImV4cCI6MTU5ODA0MDIyOSwiYXpwIjoiMFBrb1plaTVzWHV6VndHZmJGMk50bDRkN0tKT0pvamUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.d5g70-iQir_lK1tQTlT8ZPrfr684EJiJo7vnOMigKFdj7hDOBMqlIhkITTpce1J6htyI4kqtGvqjvrOkhlofE1nozIRDemQgoCA2ERIWQ70qxncad9HS2_V4oVLUr_sSBbRaWQ94iXlHJ1tnlut2JMi9TzjQAHHyYymQ6t-sXJVif8_KtL_K0GbTsPsxDx_gWagHC6JSELzhi7HOzROqPcj6dSImfiM53aW5biAb-2stYlttIyJYSUCcthrXq-ZX0Vpf1mIW54HeRBPA-OvLH1fJOKcNcDGs_mdAH0jk_NyAI_cldLawz9XHmcOD0WlHiJvx5p0ZmgQgoODsqaJyYg'
        self.casting_director_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ims5Wi0wcHQxa0pmLWFaQm5UU05HQiJ9.eyJpc3MiOiJodHRwczovL21pbXgudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmMDYzMTg5YTE1YjdiMDAxMzYxZjY1MiIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTc5NTM5NDgsImV4cCI6MTU5ODA0MDM0NywiYXpwIjoiMFBrb1plaTVzWHV6VndHZmJGMk50bDRkN0tKT0pvamUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.bmjndrpnPaEYLBV1tNYfjTQN9h-mAmEtMPqrChGSe7GL64SUOzpuFp8KAMDGnMkxuLPvnGgI954s4o2I3p2HA5aSIwjg_BY8-Eru3xiaQWYSr0ZAPYzIVg1POWrj8z1GEtjhk5VfCRCqL4qsuCEbII_bSzxhKfV2LVdrrMHqTW-tzyqV-p3-n6l68wFvCVMixIaR7w3FnA0IeuEEXRv4x28j3oDu3_YEtjUNDu5tByh-bNCNOH_AI-gxvvo5m8A0L3fjHRoJVHHv0ePLKVYYdLIAtVZA72E5XE2XyKnPBsg71Wj4NAPAjCIUf-K2CS58nbq4VwpymK6_Mxe39Y3wYA'
        self.executive_producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ims5Wi0wcHQxa0pmLWFaQm5UU05HQiJ9.eyJpc3MiOiJodHRwczovL21pbXgudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZWU1MjE5ZWZmNDU2MDAxOTMwNGM2ZiIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTc4ODQ3MTMsImV4cCI6MTU5Nzk3MTExMiwiYXpwIjoiMFBrb1plaTVzWHV6VndHZmJGMk50bDRkN0tKT0pvamUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.a3ce4GLzT7NVqFfsBmcdqAokmeG93eTeQYKcjiYB_7-MuinkTtb4zdR8_QXvmaxhkKMUtpd6hN2W_3K6oE94_cQuUo6lqb8kqysjtJ2WMOA1Gn0OCMqaALTbdAOYDEAn0SwrYVRtzqUW1HwID2SPqEKY_DZ4-pK8uJHinT5VbxW5sSPNJZkPHn49DXVNswCjMh6lIx2L6EaBwJ0IsHIGsaX2djsP3iD04K5ChwoXVQP3cI3TLYKLicAkSJ_I2zDqfRRLVaP6KkmtvouAlkw6XpZOxBkavdvOR5D1FocTLObq6jVR2cho_oTJaRa4Nji4j1lCOOGv9FYlCK9E3na3QQ'
        # Test Variables
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
