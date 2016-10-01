from datetime import datetime

from sqlalchemy import Column, DateTime, Integer

from tioeliastanoov.persistence.base import Base
from tioeliastanoov.constants import TioEliasStatus
from tioeliastanoov.exceptions import InvalidStatusError


class TioEliasStatusChange(Base):
    __tablename__ = 'tioelias_status_change'
    datetime = Column(DateTime, primary_key=True)
    status = Column(Integer, nullable=False)

    def to_status(self):
        return TioEliasStatus(self.status)


def get_latest_status(session):
    return (session
            .query(TioEliasStatusChange)
            .order_by(TioEliasStatusChange.datetime.desc())
            .first())


def change_status(session, new_status):
    try:
        TioEliasStatus(new_status)
    except ValueError:
        raise InvalidStatusError
    session.add(TioEliasStatusChange(datetime=datetime.utcnow(),
                                     status=new_status))

