from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#port 5432
engine = create_engine('postgresql://postscript_test_master:D38w7KUSFTYVKglMV@postscript-test.c8mcl9ijqgt7.us-east-2.rds.amazonaws.com/postscript_test')
Session = sessionmaker(bind=engine)

Base = declarative_base()