# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import resolve, reverse
from django.test import TestCase

from .views import signup
from .forms import SignUpForm

# Create your tests here.


class SignUpTests(TestCase):
    def SetUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        url = reverse('signup')
        self.response = self.client.get(url)
        self.assertEquals(self.response.status_code, 200)

    # if the URL /signup/ is returning the correct view function.
    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)

    def test_csrf(self):
        url = reverse('signup')
        self.response = self.client.get(url)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        url = reverse('signup')
        self.response = self.client.get(url)
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)


class SignUpFormTest(TestCase):
    def test_form_has_fields(self):
        form = SignUpForm()
        expected = ['username', 'email', 'password1', 'password2',]
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)


# testing a successful sign up.
class SuccessfulSignUpTests(TestCase):
    def SetUp(self):
        url = reverse('signup')
        data = {
            'username': 'brown',
            'email': 'test@mail.ch',
            'password1': 'abc77',
            'password2': 'abc77',
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    # A valid form submission should redirect the user to the home page
    def test_redirection(self):
        home_url = reverse('home')
        response = self.client.get(home_url)
        self.assertRedirects(response, home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        home_url = reverse('home')
        response = self.client.get(home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

    def test_form_inputs(self):
        url = reverse('signup')
        self.response = self.client.get(url)
        self.assertContains(self.response, '<input', 17)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class InvalidSignUpTests(TestCase):
    def SetUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})  # submitting empty dict

    # invalidform should return to same page so 200
    def test_sign_status_code(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_form_errors(self):
        url = reverse('signup')
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())
