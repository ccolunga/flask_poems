import json

from tests.BaseCase import BaseCase


class TestUserSignup(BaseCase):

    def test_successful_signup(self):
        # Given
        payload = json.dumps({
            "email": "exam@gmail.com",
            "password": "strongpassword"
        })

        # When
        response = self.app.post(
            '/api/auth/signup', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(str, type(response.json['id']))
        self.assertEqual(200, response.status_code)

    def test_signup_with_non_existing_field(self):
        # Given
        payload = json.dumps({
            "username": "myusername",
            "email": "exam@gmail.com",
            "password": "strongpassword"
        })

        # When
        response = self.app.post(
            '/api/auth/signup', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual('Request is missing required fields',
                         response.json['message'])
        self.assertEqual(400, response.status_code)

    def test_signup_without_email(self):
        # Given
        payload = json.dumps({
            "password": "strongpassword",
        })

        # When
        response = self.app.post(
            '/api/auth/signup', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual('Something went wrong', response.json['message'])
        self.assertEqual(500, response.status_code)

    def test_signup_without_password(self):
        # Given
        payload = json.dumps({
            "email": "exam@gmail.com",
        })

        # When
        response = self.app.post(
            '/api/auth/signup', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual('Something went wrong', response.json['message'])
        self.assertEqual(500, response.status_code)

    def test_creating_already_existing_user(self):
        # Given
        payload = json.dumps({
            "email": "exam@gmail.com",
            "password": "strongpassword"
        })
        response = self.app.post(
            '/api/auth/signup', headers={"Content-Type": "application/json"}, data=payload)

        # When
        response = self.app.post(
            '/api/auth/signup', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(
            'User with given email address already exists', response.json['message'])
        self.assertEqual(400, response.status_code)
