import names


from django.test import TestCase
from apps.account.models import User
from apps.account.backends import _authenticate_credentials
from utils import tools, messages


TEST_USERNAME = "Alibi"
TEST_USER_GMAIL = "alibi@gmail.com"
ADDRESS_TYPE = "@gmail.com"


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username=TEST_USERNAME,
            email=TEST_USER_GMAIL,
            password=tools.get_random_password(),
        )

    @staticmethod
    def get_email_and_name():
        name = names.get_first_name()
        email = name + ADDRESS_TYPE
        return name, email

    def test_create_user(self):
        name, email = UserTestCase.get_email_and_name()
        user = User.objects.create_user(
            username=name, email=email, password=tools.get_random_password()
        )
        self.assertEqual(user.username, name)
        self.assertEqual(user.email, email)
        self.assertEqual(user.is_superuser, False)

    def test_create_user_without_username(self):
        email = names.get_last_name() + ADDRESS_TYPE
        try:
            User.objects.create_user(
                None, email=email, password=tools.get_random_password()
            )
        except TypeError as error:
            self.assertEqual(str(error), messages.USERNAME_DOESNT_FILLED)

    def test_create_superuser_without_password(self):
        name, email = UserTestCase.get_email_and_name()
        try:
            User.objects.create_superuser(name, email, None)
        except TypeError as error:
            self.assertEqual(str(error), messages.SUPERUSER_MUST_HAVE_A_PASSWORD)

    def test_create_super_user(self):
        name, email = UserTestCase.get_email_and_name()
        user = User.objects.create_superuser(
            username=name, email=email, password=tools.get_random_password()
        )
        self.assertEqual(user.username, name)
        self.assertEqual(user.email, email)
        self.assertNotEqual(user.is_superuser, False)

    def test_token(self):
        (
            user_after_login,
            token,
        ) = _authenticate_credentials(self.user.token)
        self.assertEqual(user_after_login.is_active, True)
        self.assertEqual(self.user, user_after_login)

    def test_str(self):
        self.assertEqual(str(self.user), TEST_USER_GMAIL)
