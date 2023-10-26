from django.contrib.auth import get_user
from django.test import TestCase
from users.models import CustomUser
from django.urls import reverse

# Create your tests here.


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            "/users/register/",
            data={
                "username": "username",
                "first_name": "first_name",
                "last_name": "last_name",
                "email": "email@gmail.com",
                "password": "password"
            }
        )
        user = CustomUser.objects.get(username='username')

        self.assertEqual(user.first_name, 'first_name')
        self.assertEqual(user.last_name, 'last_name')
        self.assertEqual(user.email, 'email@gmail.com')
        self.assertNotEquals(user.password, "password")


class LoginTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username='gofa', first_name='gofa')
        self.db_user.set_password('gofajan')
        self.db_user.save()


    def test_succesful_login(self):
        self.client.post(reverse('users:login'),
                    data={
                        'username': 'gofa',
                        'password': 'gofajan'
                    }
            )
        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(reverse('users:login'),
                    data={
                        'username': 'gofa',
                        'password': 'gofajanx'
                    }
            )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_wrog_pass(self):
        self.client.post(reverse('users:login'),
                    data={
                        'username': 'gofax',
                        'password': 'gofajan'
                    }
            )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)



    def test_logout(self):
        self.client.login(username="gofa", password="gofajan")
        self.client.get(reverse("users:logout"))

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)





class PprofileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:login')+"?next=/users/profile/")

    def test_user_detail(self):
        user = CustomUser.objects.create(
            username='gofajan',
            first_name='gofajan',
            last_name='asadov',
            email='gofa@gmail.com',

        )
        user.set_password('gofajan')
        user.save()

        self.client.login(username='gofajan', password='gofajan')

        response = self.client.get(reverse('users:profile'))

        self.assertContains(response, user.username)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(
            username='gofa', first_name='gofajan', last_name='asadov', email='asadov@gmail.com'
        )
        user.set_password('gofajan')
        user.save()
        self.client.login(username='gofa', password='gofajan')

        response = self.client.post(
            reverse('users:profile_edit'),
            data={
                'username': 'gofajan'
            }
        )

        user.refresh_from_db()

        self.assertEqual(user.username, 'gofajan')



