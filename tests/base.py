from tioeliastanoov.app import app
from tioeliastanoov.persistence import Base

from flask_testing import TestCase


class BaseTestCase(TestCase):
    render_templates = False

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        Base.metadata.create_all()

    def tearDown(self):
        Base.metadata.drop_all()

