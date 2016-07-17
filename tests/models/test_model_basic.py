# -*- coding: utf-8 -*-


import unittest
from app import create_app, db


class ModelBasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
