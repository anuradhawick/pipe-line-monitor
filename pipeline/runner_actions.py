import dbmodels.models as dbm
import logger
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbmodels.models import Job

engine = create_engine(
    'sqlite:///' + os.getcwd() + '/db/database.db', echo=False)

Session = sessionmaker(bind=engine)
session = Session()

# get array of ready jobs
def getOneReadyJob():
    return session.query(Job).filter(Job.current_state == 'ready').first()
