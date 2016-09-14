from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, DateTime, Integer


engine = create_engine('sqlite:///:memory:')
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)


class TioEliasStatusChange(Base):
    __tablename__ = 'tioelias_status_change'
    datetime = Column(DateTime, primary_key=True)
    status = Column(Integer, nullable=False)

