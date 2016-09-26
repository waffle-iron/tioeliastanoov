from unittest import TestCase

from tioeliastanoov.app import app
from tioeliastanoov.persistence import Base


class BaseTestCase(TestCase):
    def setUp(self):
        Base.metadata.create_all()
        self.app = app.test_client()

    def tearDown(self):
        Base.metadata.drop_all()

