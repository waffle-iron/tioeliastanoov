from alchemytools.context import managed

from tioeliastanoov.persistence import (change_status, get_latest_status,
                                        Session, TioEliasStatusChange)
from tioeliastanoov.constants import TioEliasStatus

from tests.base import BaseTestCase


class TestPOST(BaseTestCase):
    def test_invalid_status(self):
        self.assertEqual(self.app.post('/').status_code, 400)

        r = self.app.post('/', data={'blargh': 6})
        self.assertEqual(r.status_code, 400)

        r = self.app.post('/', data={'status': 6})
        self.assertEqual(r.status_code, 400)

        r = self.app.post('/', data={'status': 'asdf'})
        self.assertEqual(r.status_code, 400)

    def test_change_status(self):
        status1 = TioEliasStatus.unavailable.value
        r = self.app.post('/', data={'status': status1})
        self.assertEqual(r.status_code, 200)

        with managed(Session) as s:
            last_statuses = (s.query(TioEliasStatusChange)
                             .order_by(TioEliasStatusChange.datetime.asc())
                             .all())
            self.assertEqual(len(last_statuses), 1)
            self.assertEqual(last_statuses[0].status, status1)

        status2 = TioEliasStatus.available.value
        r = self.app.post('/', data={'status': status2})
        self.assertEqual(r.status_code, 200)

        with managed(Session) as s:
            last_statuses = (s.query(TioEliasStatusChange)
                             .order_by(TioEliasStatusChange.datetime.asc())
                             .all())
            self.assertEqual(len(last_statuses), 2)
            self.assertEqual(last_statuses[0].status, status1)
            self.assertEqual(last_statuses[1].status, status2)


class TestGET(BaseTestCase):
    def test_get(self):
        status = TioEliasStatus.available.value
        with managed(Session) as s:
            change_status(s, status)

        r = self.app.get('/')
        with managed(Session) as s:
            self.assertEqual(r.status_code, 200)
            self.assertEqual(self.get_context_variable('status'), status)
            self.assertEqual(self.get_context_variable('latest_update'),
                             get_latest_status(s).datetime)
            self.assert_template_used('index.html')

