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


# Create pipeline execution
def createPipelineExecution(pipeline_executor, start_time, end_time, elapsed_time, pipeline):
    pipeline_execution = dbm.PipeLineExecution(
        pipeline_executor = pipeline_executor,
        start_time = start_time,
        end_time = end_time,
        elapsed_time = elapsed_time,
        pipeline_id = pipeline.id
    )
    session.add(pipeline_execution)
    session.commit()

    logger.log('PipeLine executor ' + pipeline_executor + ' created', 'INFO')

    return pipeline_execution


# Create job execution
def createJobExecution(current_state, job, start_time, end_time, elapsed_time, exit_status):
    job_execution = dbm.JobExecution(
        current_state = current_state,
        job_id = job.id,
        start_time = start_time,
        end_time = end_time,
        elapsed_time = elapsed_time,
        exit_status = exit_status
    )
    session.add(job_execution)
    session.commit()

    logger.log('Job execution for job ' + str(job.id) + ' was created with status ' +  current_state, 'INFO')

    return job_execution


# Update job execution
def updateJobExecution(job_execution, new_current_state):
    previous_state = job_execution.current_state
    job_execution.current_state = new_current_state
    session.commit()

    logger.log('Status of job execution ' + str(job_execution.id) + ' was updated from ' + previous_state + ' to ' +  new_current_state, 'INFO')


# Add job execution to pipeline
def addJobExecutionToPipelineExecution(pipeline_execution, job_execution):
    pipeline_execution.job_executions.append(job_execution)
    logger.log('Job execution ' +  str(job_execution.id) + ' was added to pipeline execution ' + str(pipeline_execution.id), 'INFO')


# Link job to job
def linkJobToJob(parent_job, child_job):
    child_job.parents.append(parent_job)
    session.commit()
    logger.log('Job ' +  str(child_job.id) + ' linked to job ' + str(child_job.id), 'INFO')


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
job_1 = createJob('job1', 123, 123, 345, '22dff2', 'dfgfd')
print '-------Job1 id ' + str(job_1.id) + ' created'

job_2 = createJob('job2', 1323, 1233, 3453, 'hkkjh', 'eyeyrty')
print '-------Job2 id ' + str(job_2.id) + ' created'

pipeline = createPipeline('Test pipleline', 'Vijini')
print '-------Pipeline id ' + str(pipeline.id) + ' created'

linkJobToPipeline(job_1, pipeline)
print '-------Pipeline of job ' + str(job_1.id) + ' is pipeline.id' + str(job_1.pipeline_id)
print '-------Jobs in pipeline are ' + str(pipeline.roots)

linkJobToPipeline(job_1, pipeline)

linkJobToJob(job_1, job_2)
print '-------Parents of job ' + str(job_2.id) + ' are ' + str(job_2.parents)

pipeline_execution = createPipelineExecution('ASDFGHJ', 345, 34545, 34454, pipeline)
print '-------Pipeline execution ' + pipeline_execution.pipeline_executor + ' was created'

job_execution = createJobExecution('Ready', job_1, 1000, 2000, 1000, 0)
print '-------Job execution ' + str(job_execution.job_id) + ' was created with status ' + job_execution.current_state

updateJobExecution(job_execution, 'Started')
print '-------Status of job execution ' + str(job_execution.job_id) + ' was updated to ' + job_execution.current_state

addJobExecutionToPipelineExecution(pipeline_execution, job_execution)
print '-------Job executions in pipeline execution are ' + str(pipeline_execution.job_executions)