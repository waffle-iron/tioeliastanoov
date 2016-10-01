import sys
from datetime import datetime

from alchemytools.context import managed

from tioeliastanoov.persistence.base import Base, Session
from tioeliastanoov.persistence.status_change import TioEliasStatusChange


def bootstrap(status):
    Base.metadata.create_all()
    with managed(Session) as s:
        s.add(TioEliasStatusChange(status=status, datetime=datetime.utcnow()))


if __name__ == '__main__':
    status = int(sys.argv[1])
    bootstrap(status)

