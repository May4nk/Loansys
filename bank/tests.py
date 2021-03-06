import json
from django.urls import reverse
from rest_framework.test import APITestCase,APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

#from .models import Users,Requests
#from .serializer import UserSerializer,RequestSerializer

#------------------------------------------------

client = APIClient()
class UserTest(APITestCase):
    def test_user_viewall(self):
        data ={
                "username": "admin",
                "email":"admin@gmail.com",
                "aadhar_id":123456789012,
                "role":"Admin",
                "cell_no":1234567890,
                "password":1234,
                "password2":1234,
                "name":"admin",
                'PAN_no':'JADKJ1234S'
        }
        response=self.client.post('/register/', data=data)

        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION = "Token " + token)
        response1 = self.client.get('/users/')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)


    def test_user_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def user_profile_detail_retriever(self):
        response = self.client.get('/user/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], 'admin')


#---------------------------------------------------------------

class RequestTest(APITestCase):
    
    def setUp(self):
        data ={
                "username": "admin",
                "email":"admin@gmail.com",
                "aadhar_id":123456789012,
                "role":"Admin",
                "cell_no":1234567890,
                "password":1234,
                "password2":1234,
                "name":"admin",
                'PAN_no':'JADKJ1234S'
                }
        data1 ={
                "username": "arun",
                "email":"arun@gmail.com",
                "aadhar_id":123456789012,
                "role":"Agent",
                "cell_no":1234567890,
                "password":1234,
                "password2":1234,
                "name":"admin",
                'PAN_no':'JADKJ1234S'
                }
        user2 ={
                "user_name": "ankur",
                "email":"ankur@gmail.com",
                "aadhar_id":123456789012,
                "role":"User",
                "cell_no":1234567890,
                "password":1234,
                "password2":1234,
                "name":"ankur",
                'PAN_no':'JADKJ1234S'
                }
        response = self.client.post('/register/', data=data)
        response1 = self.client.post('/register/', data=data1)
        response2 = self.client.post('/register/', data=data2)
        token = response.data['token']
        token1 = response1.data['token']
        token2 = response2.data['token']
        self.client.credentials(HTTP_AUTHORIZATION = "Token " + token)
        self.client.credentials(HTTP_AUTHORIZATION = "Token " + token1)
        self.client.credentials(HTTP_AUTHORIZATION = "Token " + token2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def making_request(self):
        data = {
                'user_name':3,
                'agent_name':2,
                'loan_amt':20000,
                'interest_rate':10,
                'EMI':1000,
                'total_months':20
                }
        responsen=self.client.post('/requests/',data=data)
        self.assertEqual(responsen.status_code, status.HTTP_200_OK)

