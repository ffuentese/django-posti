import os, time
from django.test import TestCase, override_settings
from posti.forms import PostForm
from django.urls import reverse
from posti.models import Post
import django.urls
from django.contrib.auth.models import User
from django.core import mail
from django.contrib.auth.forms import UserCreationForm




# Create your tests here.

def create_post():
    """
    Creates anonymous post
    :rtype : Post
    """
    data = {'title': 'Esto es un titulo', 'text': 'Esto es un texto de prueba'}
    post = Post.create_post(data['title'], data['text'])
    post.save()
    return post

def create_post_with_user(user):
    """
    Creates anonymous post
    :rtype : Post
    """
    data = {'title': 'Esto es un titulo', 'text': 'Esto es un texto de prueba'}
    post = Post.create_post(data['title'], data['text'])
    post.user = user
    post.save()
    return post

class PostFormTests(TestCase):

    def setUp(self):
        os.environ['NORECAPTCHA_TESTING'] = 'True'

    def test_create_post_with_no_title(self):
        """
        A form with no title should not be valid
        :return:
        """
        data = {'title': '', 'text': 'Esto es un texto de prueba', 'g-recaptcha-response': 'PASSED'}
        f = PostForm(initial=data)
        self.assertFalse(f.is_valid())

    def test_create_post(self):
        """
        A form with title should be valid
        :return:
        """
        data = {'title': 'Esto es un título', 'text': 'Esto es un texto de prueba', 'g-recaptcha-response': 'PASSED'}
        f = PostForm(data)
        self.assertTrue(f.is_valid())

    def test_create_post_without_recaptcha(self):
        """
        A form with no recaptcha should not be valid
        :return:
        """
        data = {'title': 'Esto es un título', 'text': 'Esto es un texto de prueba', 'g-recaptcha-response': 'NOT PASSED'}
        f = PostForm(data)
        self.assertFalse(f.is_valid())

    def tearDown(self):
        os.environ['NORECAPTCHA_TESTING'] = 'False'


class PostViewTests(TestCase):
    def setUp(self):
        os.environ['NORECAPTCHA_TESTING'] = 'True'
        self.test_user = User.objects.create_user('test_user', 'email@ffuent.es', 'Cr4zy#P4ssw0rd')
        self.test_user2 = User.objects.create_user('test_user2', 'correo@ffuent.es', 'N0tSoCr4zy#P4ssw0rd')

    def tearDown(self):
        os.environ['NORECAPTCHA_TESTING'] = 'False'
        self.test_user.delete()
        self.test_user2.delete()

    def test_adding_post_with_no_title(self):
        data = {'title': '', 'text': 'Esto es un texto de prueba', 'g-recaptcha-response': 'PASSED'}
        response = self.client.post(reverse('posti:add'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please fill out all the fields")

    def test_adding_post_with_title(self):
        data = {'title': 'Esto es un titulo', 'text': 'Esto es un texto de prueba', 'g-recaptcha-response': 'PASSED'}
        response = self.client.post(reverse('posti:add'), data, follow=True)
        self.assertContains(response, data['title'])

    def test_adding_post_without_captcha(self):
        data = {'title': 'Esto es un titulo', 'text': 'Esto es un texto de prueba', 'g-recaptcha-response': 'NOT PASSED'}
        response = self.client.post(reverse('posti:add'), data, follow=True)
        self.assertNotContains(response, data['title'])

    def test_updating_post_with_no_title(self):
        """
        A post with no title should not be saved
        :return:
        """
        p = create_post()
        data = {'title': '', 'text': 'Esto es un texto de prueba'}
        response = self.client.post(django.urls.reverse('posti:update', args=(p.uuid,)), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No title in form")

    def test_updating_post(self):
        p = create_post()
        data = {'title': 'Esto es OTRO titulo', 'text': 'Esto es un texto de prueba'}

        response = self.client.post(django.urls.reverse('posti:update', args=(p.uuid,)), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, data['title'])

    def test_deleting_post_not_belonging_to_user(self):
        p = create_post_with_user(self.test_user)
        self.client.force_login(self.test_user2)
        data = {'uuid': p.uuid}
        response = self.client.post(django.urls.reverse('posti:delete'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Post does not belong to the user.")

    def test_updating_post_not_belonging_to_user(self):
        p = create_post_with_user(self.test_user)
        self.client.force_login(self.test_user2)
        data = {'title': 'Esto es un titulo', 'text': 'Esto NO debería publicarse'}
        response = self.client.post(django.urls.reverse('posti:update', args=(p.uuid,)), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Post does not belong to the user.")

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_reporting_post(self):
        p = create_post()
        response = self.client.get(reverse('posti:report', args=(p.uuid,)))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(mail.outbox) == 1)

    def test_signup(self):
        """
        Test last
        :return:
        """
        data = {'username': 'test_user3_destroy', 'password1': 'myP4assw0rd.', 'password2': 'myP4assw0rd.'}
        response = self.client.post(reverse('posti:signup'), data, follow=True)
        self.assertContains(response, 'Bienvenido test_user3_destroy')
