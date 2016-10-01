from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from tioeliastanoov.conf import DB_URL


engine = create_engine(DB_URL)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

