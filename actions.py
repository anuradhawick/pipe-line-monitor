import dbmodels.models as dbm
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine(
    'sqlite:///' + os.getcwd() + '/db/database.db', echo=False)

Session = sessionmaker(bind=engine)
session = Session()


def createJobsAndPipe():
    p = dbm.PipeLine(
        pipeline_name="Test Pipe",
        pipeline_owner="Anuradha"
    )
    session.add(p)

    j1 = dbm.Job(
        command="ls -la",
        required_memory=1024,
        required_wall_time=100,
        required_cpus=16,
        required_modules="a,b,c",
        unique="unique",
    )
    session.add(j1)

    j2 = dbm.Job(
        command="ssh r",
        required_memory=1024,
        required_wall_time=100,
        required_cpus=2,
        required_modules="a,b,c",
        unique="unique",
    )
    session.add(j2)

    j3 = dbm.Job(
        command="rm -rf test",
        required_memory=1024,
        required_wall_time=100,
        required_cpus=8,
        required_modules="a,b,c",
        unique="unique",
    )
    session.add(j3)

    j2.parents.append(j1)

    j2.children.append(j3)

    p.roots = [j1]
    session.commit()
