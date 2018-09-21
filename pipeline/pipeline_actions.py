import db_utils.models as dbm
import logger
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import db_utils.utils as utils

session = utils.get_session()

# Create pipeline


def create_pipeline(pipeline_name, pipeline_owner):
    pipeline = dbm.PipeLine(
        pipeline_name=pipeline_name,
        pipeline_owner=pipeline_owner
    )
    session.add(pipeline)
    session.commit()

    logger.log('Pipline ' + pipeline_name +
               ' created with id ' + str(pipeline.id), 'INFO')

    return pipeline


# Create job
def create_job(command, required_memory, required_wall_time, required_cpus, required_modules, unique):
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

    logger.log('Job for command ' + command +
               ' created with id ' + str(job.id), 'INFO')

    return job


# Create pipeline execution
def create_pipeline_execution(pipeline_executor, start_time, end_time, elapsed_time, pipeline):
    pipeline_execution = dbm.PipeLineExecution(
        pipeline_executor=pipeline_executor,
        start_time=start_time,
        end_time=end_time,
        elapsed_time=elapsed_time,
        pipeline_id=pipeline.id
    )
    session.add(pipeline_execution)
    session.commit()

    logger.log('Pipeline execution ' + pipeline_executor +
               ' created with id ' + str(pipeline_execution.id), 'INFO')

    return pipeline_execution


# Create job execution
# TODO integrate pipeline relation ship
def create_job_execution(job, start_time, end_time, elapsed_time, exit_status):
    job_execution = dbm.JobExecution(
        start_time=start_time,
        end_time=end_time,
        elapsed_time=elapsed_time,
        exit_status=exit_status
    )
    job.current_execution = job_execution
    session.add(job_execution)
    session.commit()

    logger.log('Job execution for job ' + str(job.id), 'INFO')

    return job_execution


# Update job execution, at the end of execution
def update_job_execution(job_execution, end_time, elapsed_time, exit_status):
    job_execution.end_time = end_time
    job_execution.elapsed_time = elapsed_time
    job_execution.exit_status = exit_status

    session.commit()

    logger.log('Status of job execution ' + str(job_execution.id) +
               ' was updated end time ' + str(end_time) + ' with elapsed time ' + str(elapsed_time) + ' exit status ' + str(exit_status), 'INFO')


# Add job execution to pipeline
def add_job_execution_to_pipeline_execution(pipeline_execution, job_execution):
    pipeline_execution.job_executions.append(job_execution)
    logger.log('Job execution ' + str(job_execution.id) +
               ' was added to pipeline execution ' + str(pipeline_execution.id), 'INFO')


# Link job to job
def link_job_to_job(parent_job, child_job):
    child_job.parents.append(parent_job)
    session.commit()
    logger.log('Job ' + str(child_job.id) +
               ' linked to job ' + str(parent_job.id), 'INFO')

# Set job as ready


def set_job_as_ready(job):
    job.current_state = 'ready'
    session.commit()
    logger.log('Job ' + str(job.id) +
               ' marked ready', 'INFO')

# Set job as running


def set_job_as_running(job):
    job.current_state = 'running'
    session.commit()
    logger.log('Job ' + str(job.id) +
               ' marked running', 'INFO')

# Set job as completed


def set_job_as_completed(job):
    job.current_state = 'completed'
    job.current_execution = None
    session.commit()
    logger.log('Job ' + str(job.id) +
               ' marked completed', 'INFO')
        

# Set job as failed


def set_job_as_failed(job):
    job.current_state = 'failed'
    session.commit()
    logger.log('Job ' + str(job.id) +
               ' marked failed', 'INFO')

# Update jobs eligibility to run


def update_next_ready_jobs(completed_job):
    # get next set of jobs
    children = completed_job.children

    # for each child
    for child in children:
        parents = child.parents
        parent_ok = True
        
        # check if parents have completed
        for parent in parents:
            if parent.current_state != 'completed':
                parent_ok = False
                break
        if parent_ok:
            set_job_as_ready(child)

# Link job to pipeline


def link_job_to_pipeline(job, pipeline):
    job.pipleine_id = pipeline.id
    session.add(job)

    present = False

    for root in pipeline.roots:
        if job.id == root.id:
            present = True
            break

    if present == True:
        logger.log('Job run id ' + str(job.id) +
                   ' already exists in the pipeline ' + str(pipeline.id), 'WARNING')
    else:
        pipeline.roots.append(job)
        logger.log('Job run id ' + str(job.id) +
                   ' added to pipeline ' + str(pipeline.id), 'INFO')

    session.commit()

# get array of ready jobs


def get_one_ready_job():
    return session.query(dbm.Job).filter(dbm.Job.current_state == 'ready').first()
