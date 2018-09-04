from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from dbmodels.jobs import Job, PipeLine

engine = create_engine(
    'sqlite:////media/admin-u6776114/data/pipe-mgr/db/database.db', echo=False)

Session = sessionmaker(bind=engine)
session = Session()

# job = Job(command="child sample command")
# session.add(job)
# session.commit()

# pipe = PipeLine()
# session.add(pipe)
# session.commit()

# parentJob = ''
# childJb = ''

# for job in session.query(Job).filter(Job.id == 1):
#     parentJob = job

#     # print parentJob
#     # print parentJob.command
#     # print parentJob.children[0].parent.command

# for job in session.query(Job).filter(Job.id != 1):
#     childJb = job

# parentJob.childJobs.append(childJb)

# pipe.roots.append(parentJob)

# session.commit()