from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Datetime, Integer


engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class TioEliasStatusChange(Base):
    datetime = Column(Datetime, primary_key=True)
    status = Column(Integer, nullable=False)

