# -*- coding: utf-8 -*-

from app.models.users import User
from tests.models.test_model_basic import ModelBasicsTestCase


class UserModelTestCase(ModelBasicsTestCase):

    def test_password_setter(self):
        u = User(password="cat")
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password="cat")
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password="cat")
        self.assertTrue(u.verify_password("cat"))
        self.assertFalse(u.verify_password("dog"))

    def test_password_salts_are_random(self):
        u = User(password="cat")
        u2 = User(password="cat")
        self.assertTrue(u.password_hash!=u2.password_hash)

    def test_add_new_user_and_get_by_email(self):
        User.add_new_user(email="cat", password="cat")
        u = User.get_user_by_email("cat")
        self.assertFalse(u is None)
        self.assertTrue(User.get_user_from_email("dog") is None)


