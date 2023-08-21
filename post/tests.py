from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from authenticate.serializers import UserRegistrationSerializer

User = get_user_model()


class WeekRangeListApiViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # initialize some users
        register_url = reverse('authenticate:register')
        response_1 = self.client.post(register_url, data={'username': 'amir', 'password': '123',
                                                          'password2': '123'})
        response_2 = self.client.post(register_url, data={'username': 'sajjad', 'password': '13sajjad',
                                                          'password2': '123'})
        response_3 = self.client.post(register_url, data={'username': 'mammad', 'password': 'mami'})

    def test_create_post(self):
        url = reverse('post:')  # Assuming you're using djoser's TokenObtainPairView
        # data = {
        #     'username': 'shayan',
        #     'password': '123',
        # }
        # user_obj = User.objects.get(username='shayan')
        # # print(user_obj.id)
        # response = self.client.post(url, data, format='json')
        # self.assertIn('token', response.data)
        # token_key_db = Token.objects.get(user_id=user_obj.id)
        # self.assertEqual(response.data.get('token'), token_key_db.key)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertIn('access', response.data)
        # self.assertIn('refresh', response.data)