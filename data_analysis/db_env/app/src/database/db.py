from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

data = open('../../db_info.txt').readlines()[0]

engine = create_engine(data)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()