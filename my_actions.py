import dbmodels.models as dbm
import logger
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# engine = create_engine(
#     'sqlite:////media/admin-u6776114/data/pipe-mgr/db/database.db', echo=False)

engine = create_engine(
    'sqlite:////media/admin-u6776102/data/Pipeline Project/pipe-line-monitor/db/database.db', echo=False)

Session = sessionmaker(bind=engine)
session = Session()


# Create pipeline
def createPipeline(pipeline_name, pipeline_owner):
    pipeline = dbm.PipeLine(
        pipeline_name=pipeline_name,
        pipeline_owner=pipeline_owner
    )
    session.add(pipeline)
    session.commit()

    logger.log('Pipline ' +  pipeline_name + ' created', 'INFO')

    return pipeline


# Create job
def createJob(command, required_memory, required_wall_time, required_cpus, required_modules, unique):
    job = dbm.Job(
        command=command,
        required_memory=required_memory,
        required_wall_time=required_wall_time,
        required_cpus=required_cpus,
        required_modules=required_modules,
        unique=unique,
    )
    session.add(job)
    session.commit()

    logger.log('Job for command ' +  command + ' created', 'INFO')

    return job


# Create job run
def createJobRun(current_state, job, pipeline, start_time, end_time, elapsed_time, exit_status):
    jobRun = dbm.JobRun(
        current_state = current_state,
        job_id = job.id,
        pipeline_id = pipeline,
        start_time = start_time,
        end_time = end_time,
        elapsed_time = elapsed_time,
        exit_status = exit_status
    )
    session.add(jobRun)
    session.commit()

    logger.log('Job run with status ' +  current_state + ' created', 'INFO')

    return jobRun


# Link job to job
def linkJobToJob(job1, job2):
    job2.parents.append(job1)
    session.commit()
    logger.log('Job ' +  str(job2.id) + ' linked to job ' + str(job2.id), 'INFO')


# Link job to pipeline
def linkJobToPipeline(job, pipeline):
    job.pipleine_id = pipeline.id
    session.add(job)

    present = False

    for root in pipeline.roots:
        if job.id == root.id:
            present = True
            break

    if present == True:
        logger.log('Job run id ' +  str(job.id) + ' already exists in the pipeline', 'WARNING')
    else:
        pipeline.roots.append(job)
        logger.log('Job run id ' +  str(job.id) + ' added to pipeline', 'INFO')

    session.commit()


# Test
job1 = createJob('job1', 123, 123, 345, '22dff2', 'dfgfd')
print 'Job1 id ' + str(job1.id) + ' created'

job2 = createJob('job2', 1323, 1233, 3453, 'hkkjh', 'eyeyrty')
print 'Job2 id ' + str(job2.id) + ' created'

pipeline = createPipeline('Test pipleline', 'Vijini')
print 'Pipeline id ' + str(pipeline.id) + ' created'

linkJobToPipeline(job1, pipeline)
print 'Pipeline of job ' + str(job1.id) + ' is pipeline.id' + str(job1.pipeline_id)
print pipeline.roots

linkJobToJob(job1, job2)
print 'Parents of job ' + str(job2.id) + ' are ' + str(job2.parents)