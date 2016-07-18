# -*- coding: utf-8 -*-


from tests.test_basics import BasicsTestCase
from flask import url_for
from app.models.users import User


class AuthTestCase(BasicsTestCase):

    def test_register_and_login(self):
        with self.app.test_client() as client:
            response = client.get(url_for("main.admin"))
            self.assertEqual(response.location[-6:], url_for("auth.login"))
            response = client.post(url_for("auth.register"), data={
                "email": "example@example.com",
                "password": "cat",
                "password2": "cat",
            })
            self.assertEqual(response.location[-6:], url_for("auth.login"))
            self.assertTrue(User.get_user_by_email("example@example.com") is not None)
            client.post(url_for("auth.login"), data={
                "email": "example@example.com",
                "password": "cat"
            })
            response = client.get(url_for("main.admin"))
            self.assertEqual(response.status_code, 200)

            client.get(url_for("auth.logout"))
            response = client.get(url_for("main.admin"))
            self.assertEqual(response.location[-6:], url_for("auth.login"))
