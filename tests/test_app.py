from alchemytools.context import managed

from tioeliastanoov.persistence import Session, TioEliasStatusChange
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
