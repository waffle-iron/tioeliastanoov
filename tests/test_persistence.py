from datetime import datetime
from unittest import TestCase, main

from alchemytools.context import managed
from freezegun import freeze_time

from tioeliastanoov.exceptions import InvalidStatusError
from tioeliastanoov.persistence import (Base, change_status, Session,
                                        TioEliasStatusChange)
from tioeliastanoov.constants import TioEliasStatus


class TestChangeStatus(TestCase):
    def setUp(self):
        Base.metadata.create_all()

    def tearDown(self):
        Base.metadata.drop_all()

    def test_invalid_stats(self):
        with managed(Session) as s:
            self.assertRaises(InvalidStatusError, change_status, s, 0)
            self.assertRaises(InvalidStatusError, change_status, s, 5)
            self.assertRaises(InvalidStatusError, change_status, s, -1)

    @freeze_time(datetime.utcnow())
    def test_change_status(self):
        with managed(Session) as s:
            change_status(s, TioEliasStatus.unavailable.value)

        with managed(Session) as s:
            status_change = s.query(TioEliasStatusChange).one()
            self.assertEqual(status_change.datetime, datetime.utcnow())
            self.assertEqual(status_change.status,
                             TioEliasStatus.unavailable.value)


