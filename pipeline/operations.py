from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine(
    'sqlite:////media/admin-u6776114/data/pipe-mgr/db/database.db', echo=False)

Session = sessionmaker(bind=engine)
session = Session()

def createJob(jobObj):
    session.add(jobObj)
    session.commit()

def addChildJob(parentJob, childJob):
    parentJob.children.append(childJob)
    session.commit()

def createPipeline(pipelineObj):
    session.add(pipelineObj)
    session.commit()

def setPipeRoots(pipeline, rootsArray):
    pipeline.roots = rootsArray
    session.commit()