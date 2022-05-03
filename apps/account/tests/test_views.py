# import names
#
# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from django.urls import reverse
#
# from rest_framework.test import APIClient
# from rest_framework import status
#
# from utils import tools
#
# c = APIClient()
#
# User = get_user_model()
#
# TEST_USERNAME = 'test1'
# TEST_EMAIL = 'test1@gmail.com'
# TEST_PASSWORD = 'test12345'
#
#
# class BaseTestCase(TestCase):
#
#     def post(self, url, params, expected_status, headers=None):
#         response = c.post(url, params, format='json', headers=headers)
#         self.assertEqual(response.status_code, expected_status)
#         # print(res)
#
#
# class CoreViewTestCase(BaseTestCase):
#
#     def setUp(self):
#         self.user = User.objects.create_user(username=TEST_USERNAME, password=TEST_PASSWORD, email=TEST_EMAIL)
#
#     def test_register(self):
#         url = reverse('account:register-list')
#         data = {
#             "email": names.get_first_name() + '@gmail.com',
#             "username": names.get_first_name(),
#             "password": tools.get_random_password()
#         }
#         self.post(url, data, status.HTTP_201_CREATED)
#
#     def test_login(self):
#         url = reverse('account:login-list')
#         data = {
#             "email": self.user.email,
#             "password": TEST_PASSWORD
#         }
#         self.post(url, data, status.HTTP_201_CREATED)
#
#     def test_change_password(self):
#         url = reverse('account:change_password-list')
#         data = {
#             "old_password": TEST_PASSWORD,
#             "new_password": tools.get_random_password(),
#             "new_password_confirm": tools.get_random_password()
#         }
#         headers = {
#             'HTTP_AUTHORIZATION': 'Token ' + self.user.token
#         }
#         self.post(url, data, status.HTTP_201_CREATED, headers=headers)
