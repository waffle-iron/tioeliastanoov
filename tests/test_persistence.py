from datetime import datetime
from unittest import TestCase, main

#from alchemytools.context import managed
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
        s = Session()
        self.assertRaises(InvalidStatusError, change_status, s, 0)
        self.assertRaises(InvalidStatusError, change_status, s, 5)
        self.assertRaises(InvalidStatusError, change_status, s, -1)

    @freeze_time(datetime.utcnow())
    def test_change_status(self):
        s = Session()
        change_status(s, TioEliasStatus.unavailable.value)
        s.commit()

        s = Session()
        status_change = s.query(TioEliasStatusChange).one()
        self.assertEqual(status_change.datetime, datetime.utcnow())
        self.assertEqual(status_change.status,
                         TioEliasStatus.unavailable.value)


main()
