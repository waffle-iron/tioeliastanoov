from datetime import datetime, timedelta

from alchemytools.context import managed
from freezegun import freeze_time

from tioeliastanoov.exceptions import InvalidStatusError
from tioeliastanoov.persistence import (change_status, get_latest_status,
                                        Session, TioEliasStatusChange)
from tioeliastanoov.constants import TioEliasStatus

from tests.base import BaseTestCase


class TestChangeStatus(BaseTestCase):
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


class TestGetLastStatus(BaseTestCase):
    def test_no_status(self):
        with managed(Session) as s:
            self.assertIsNone(get_latest_status(s))

    def test_only_one_status(self):
        dt = datetime.utcnow()
        with managed(Session) as s:
            s.add(TioEliasStatusChange(datetime=dt,
                                       status=TioEliasStatus.available.value))

        with managed(Session) as s:
            self.assertEqual(get_latest_status(s).datetime, dt)

    def test_multiple_statuses(self):
        status = TioEliasStatus.available.value
        with freeze_time(datetime.utcnow()) as dt:
            with managed(Session) as s:
                s.add(TioEliasStatusChange(datetime=dt.time_to_freeze,
                                           status=status))

                dt.tick(delta=timedelta(minutes=27))
                latest_dt = dt.time_to_freeze

                s.add(TioEliasStatusChange(datetime=latest_dt, status=status))

        with managed(Session) as s:
            self.assertEqual(get_latest_status(s).datetime, latest_dt)
