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

    #     self.client = APIClient()
    #
        # intialize some users
        register_url = reverse('authenticate:register')
        response = self.client.post(register_url, data={'username': 'shayan', 'password': '123',
                                                        'password2': '123'})
    # login_url = reverse('authenticate:login')

    def test_register_url(self):
        register_url = reverse('authenticate:register')
        response_1 = self.client.post(register_url, data={'username': 'amir', 'password': '123',
                                                          'password2': '123'})
        response_2 = self.client.post(register_url, data={'username': 'sajjad', 'password': '13sajjad',
                                                          'password2': '123'})
        response_3 = self.client.post(register_url, data={'username': 'mammad', 'password': 'mami'})
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_1.data.get('username'), 'amir')

    def test_login(self):
        url = reverse('authenticate:login')  # Assuming you're using djoser's TokenObtainPairView
        data = {
            'username': 'shayan',
            'password': '123',
        }
        user_obj = User.objects.get(username='shayan')
        response = self.client.post(url, data, format='json')
        self.assertIn('token', response.data)
        token_key_db = Token.objects.get(user_id=user_obj.id)
        self.assertEqual(response.data.get('token'), token_key_db.key)
