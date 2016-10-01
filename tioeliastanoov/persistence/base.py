from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///db.sqlite')
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

