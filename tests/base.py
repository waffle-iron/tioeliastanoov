from tioeliastanoov.app import app
from tioeliastanoov.persistence import Base

from flask_testing import TestCase


class BaseTestCase(TestCase):
    render_templates = False

    def create_app(self):
        return app

    def setUp(self):
        Base.metadata.create_all()
        self.app = app.test_client()

    def tearDown(self):
        Base.metadata.drop_all()

