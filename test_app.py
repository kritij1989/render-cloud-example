import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from flask import Flask, render_template, request, abort, jsonify

# TEST CASE CLASS


class CastingAgencyProjectTestClass(unittest.TestCase):

    def setUp(self):

        
        ASSISTANT_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtwSWlmTVNya3VyRzZHanV1cVhtRiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZXNob3B1ZGFjaXR5a3JpdGkudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0ZjAyOWFmYjNiYzllNjg1ZDQzZGQ5NiIsImF1ZCI6Im1vdmllcyIsImlhdCI6MTY5MzgwNDEyMywiZXhwIjoxNjkzODkwNTIzLCJhenAiOiJjNEx2cW1tTm4xblg1aVUwcFZjcnMxNFNhNTFMaExRWiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.YFtpxiwxSAspep6yIeODKD2Ki_Bas4-4GKRgg3d5suq7Mqm6RSH0F-7yFm3ldfoLw2rD7f0srn68ELGAASmq9-Z3SpVE2-N-7i4jnGZHN_2bYwSGWO1VBuyWWdxX4AfNtklPfxhaa_05y-aIZfjX5tQqegLFdEcEpZvB5BWdPmipJpeDgWj0KafRsjTGj1pFT6E8UGCeCLSffPcpxPinwvRNUQdhpi2__iirFONwA1bTxRVnhSy8AUhnDB0yuqFPQy8veiyo_-nLrM5FO1upgmZaks0ezdjC8ruZcht7FstfuqEIKvPCoqZl64zMAASCqCHP5Q4qnYRzcaAmCWYRog'
        DIRECTOR_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtwSWlmTVNya3VyRzZHanV1cVhtRiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZXNob3B1ZGFjaXR5a3JpdGkudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0ZjAyYTc5MWFmNTVhMzhhZTZlMDBkYyIsImF1ZCI6Im1vdmllcyIsImlhdCI6MTY5MzgwNDA4MiwiZXhwIjoxNjkzODkwNDgyLCJhenAiOiJjNEx2cW1tTm4xblg1aVUwcFZjcnMxNFNhNTFMaExRWiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.ko4cIIoCLjnDIYcFHUe6ttoHjncYeAEiH2oiDV2al7hk4JDDacee66jLLgyb3_O8gQX7KYHVkg706fdY2KdVTrwQcM-bUMbYayMMeCPQph3VqBkVqzlp8q1W0eHNxfoXr5uhOqTLEKK7_nOkzv345fDZ5nhakQOkQ-u3s-fWccNDiR9S14_aMEYS2nPDFsN8BQW9DshIwc7kdjnF-ozMM6pKgQOhV4_pQ48P_eodUuf-khaOmXT25eE-MgFZwE-D6rU8bugVS2Oi_3ZYZinq0P7zVyQcYorItwCu6C11kj6BK32ioN7jpSu14K6pFyauJJOsUU8NsOjpzDBaf6P-sA'
        PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtwSWlmTVNya3VyRzZHanV1cVhtRiJ9.eyJpc3MiOiJodHRwczovL2NvZmZlZXNob3B1ZGFjaXR5a3JpdGkudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0ZjAyYTEzODI3Nzc5YmE5NmVkZWQwYSIsImF1ZCI6Im1vdmllcyIsImlhdCI6MTY5MzgwNDE2NywiZXhwIjoxNjkzODkwNTY3LCJhenAiOiJjNEx2cW1tTm4xblg1aVUwcFZjcnMxNFNhNTFMaExRWiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.Hv-2cmG8EsjST0HjR1PyT9hBK5AYiWe2q_J7EoF0EuNpLJSQA_TkdEWsK0L7AVMWLwRFea2UwiDkArtkRPt-1WLZYoaInFGojFZguPymqK2fFsapRwVhvIMS_fDvczX4KHu8VBU4FxCdqOj_BlmaWAUfdqeKAV9PZtvCbWgjaITZoh09hxUnLIwXMUy-ibflp2Pj0ckOiIWePsTIOH-Fk25aqKS1AT1tTDhAaq17hlvlWVALUiZpw6AJdMrRGTrE_5cwhg0W-dLXgt6cxVpGomrUPj_Uh5Xc2qmJCnhRw03kCNW9SzgVRKLX8A-EEHUpq5h9u1oLzUcKmExpeknL9w'

        self.assistant_auth_header = {'Authorization':
                                      'Bearer ' + ASSISTANT_TOKEN}
        self.director_auth_header = {'Authorization':
                                     'Bearer ' + DIRECTOR_TOKEN}
        self.producer_auth_header = {'Authorization':
                                     'Bearer ' + PRODUCER_TOKEN}

        self.app = Flask(__name__)
        self.client = self.app.test_client


# Test data set-up for all tests down under

        self.post_actor = {
            'name': "Michael",
            'age': 45,
            'gender': 'MALE',
            'id':100
        }

        self.post_actor_name_errordata = {
            'age': 34,
            'gender': "MALE"
        }
        self.patch_actor_on_age = {
            'age': 55,
            'name':'test',
            'gender':'M'
        }

        self.post_movie = {
            'title': "Test MOVIE",
            'release_date': "2020-10-10",
            'id':100
        }       

        self.post_movie_title_error = {
            'release_date': "2030-10-10"
        }

        self.patch_movie_on_reldate = {
            'release_date': "2035-10-10",
            'title': "Test MOVIE"
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            # self.db.create_all()

    def tearDown(self):
        pass


# Test cases for the Endpoints related to /actors
# ------------------------------------------------

    # get actor positive case with assistant role
    def test_assistant_get_actors(self):
        res = self.client().get('/actors?',
                                headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # get actor positive case with director role
    def test_director_get_actors(self):
        res = self.client().get('/actors?',
                                headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

     # get actor positive case with producer role
    def test_producer_get_actors(self):
        res = self.client().get('/actors?',
                                headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

     # get actor negative case without token 
    def test_get_actors_withoutRBAC(self):
         res = self.client().get('/actors')
         data = json.loads(res.data)
         self.assertNotEqual(res.status_code, 200)


    # post actor positive case with director role
    def test_director_post_new_actor(self): 
        res = self.client().get('/actors?',
                                headers=self.producer_auth_header)
        data = json.loads(res.data)

        for x in data['actors']:
         if (x['id']==100):
             res = self.client().delete('/actors/100',
                                   headers=self.director_auth_header)       
       
        res = self.client().post('/actors',
                                 json=self.post_actor,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success']) 
           


# Add actor with missing name

     # post actor negative case with director role missing name
    def test_post_new_actor_name_missing(self):
        res = self.client().post('/actors',
                                 json=self.post_actor_name_errordata,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertNotEqual(res.status_code, 200)
        self.assertFalse(data['success'])

#     # delete actor negative case with director 
    def test_delete_actor_not_found(self):
        res = self.client().delete('/actors/999',
                                   headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertNotEqual(res.status_code, 200)
        self.assertFalse(data['success'])

   # delete actor postive case with director 
    def test_delete_actor(self):
        res = self.client().get('/actors?',
                                headers=self.producer_auth_header)
        data = json.loads(res.data)
        exist=0
        for x in data['actors']:
         if (x['id']==100):
             exist=1 

        if exist== 0:
               res = self.client().post('/actors',
                                 json=self.post_actor,
                                 headers=self.producer_auth_header)   
        
        res = self.client().delete('/actors/100',
                              headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # delete movie postive case with director 
    def test_delete_movie(self):
        res = self.client().get('/movies?',
                                headers=self.producer_auth_header)
        data = json.loads(res.data)
        exist=0
        for x in data['movies']:
         if (x['id']==100):
             exist=1 

        if exist== 0:
               res = self.client().post('/movies', json=self.post_movie,
                                 headers=self.producer_auth_header)   
        
        res = self.client().delete('/movies/100',
                              headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        

#      patch actor negative case with director  
    def test_patch_actor_not_found(self):
        res = self.client().patch('/actors/999',
                                   json=self.patch_actor_on_age,
                                   headers=self.director_auth_header)
        data = json.loads(res.data)     

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

#     # patch actor postive case with director
    def test_patch_actor(self):
        res = self.client().get('/actors?',
                                headers=self.producer_auth_header)
        data = json.loads(res.data)
        exist=0
        for x in data['actors']:
            if(x['id']==100) :
                exist=1                     
           
        if exist==0:
            res = self.client().post('/actors',
                                 json=self.post_actor,
                                 headers=self.producer_auth_header)

        res = self.client().patch('/actors/100',
                                  json=self.patch_actor_on_age,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

#     # get actor negative case without auth
    def test_get_actors_no_auth(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
       
        self.assertEqual(data['code'],
                         'No authorisation Header')
        self.assertEqual(data['description'],
                         'No authorisation Header')
        
#     # post actor negative case with assistant auth
    def test_post_actor_wrong_auth(self):
        res = self.client().post('/actors',
                                 json=self.post_actor,
                                 headers=self.assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(data['code'],
                         'unauthorized')
        self.assertEqual(data['description'],
                         'Permission not found.')

    def test_delete_actor_wrong_auth(self):
        res = self.client().delete('/actors/10',
                                   headers=self.assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(data['code'],
                         'unauthorized')
        self.assertEqual(data['description'],
                         'Permission not found.')

#     # get movies a assistant auth
    def test_get_movies(self):
        res = self.client().get('/movies',
                                headers=self.assistant_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

#     # get movies a director auth
    def test_get_movies_forDirector(self):
        res = self.client().get('/movies',
                                headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

#     # get movies a producer auth
    def test_get_movies_forProducer(self):
        res = self.client().get('/movies',
                                headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

#     # get movies a without auth
    def test_get_movies_withoutAuth(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(data['code'],
                         'No authorisation Header')
        self.assertEqual(data['description'],
                         'No authorisation Header')

#     # post movie
    def test_post_new_movie(self):
        
        res = self.client().get('/movies?',
                                headers=self.producer_auth_header)
        data = json.loads(res.data)        
        for x in data['movies']:         
            if(x['id']==100):
                res = self.client().delete('/movies/100',
                                   headers=self.producer_auth_header)
        
        res = self.client().post('/movies', json=self.post_movie,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

#     # post movie error case
    def test_post_new_movie_title_error(self):
        res = self.client().post('/movies',
                                 json=self.post_movie_title_error,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable. Check your input.')

     # delete movie error case
    def test_delete_movie_not_found(self):
        res = self.client().delete('/movies/777',
                                   headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found.')

     # patch movie postive case
    def test_patch_movie(self):
        res = self.client().get('/movies?',
                                headers=self.producer_auth_header)
        data = json.loads(res.data)
        exist=0
        for x in data['movies']:
            if(x['id']==100):
                exist=1

        if exist==0:
            res = self.client().post('/movies',
                                 json=self.post_movie,
                                 headers=self.producer_auth_header)

        res = self.client().patch('/movies/100',
                                  json=self.patch_movie_on_reldate,
                                  headers=self.producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

#      # patch movie error case
    def test_patch_movie_not_found(self):
        res = self.client().patch('/movies/99',
                                  json=self.patch_movie_on_reldate,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found.')

#      # get movie error case without auth
    def test_get_movies_no_auth(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)       
        self.assertEqual(data['code'],
                         'No authorisation Header')
        self.assertEqual(data['description'],
                         'No authorisation Header')

#      # post movie error case wrong auth
    def test_post_movie_wrong_auth(self):
        res = self.client().post('/movies', json=self.post_movie,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(data['code'],
                         'unauthorized')
        self.assertEqual(data['description'],
                         'Permission not found.')

    


# run 'python test_app.py' to start tests
if __name__ == "__main__":
    unittest.main()