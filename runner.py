import time

import pipeline.pipeline_actions as actions
from subprocess import run
import db_utils.utils as utils

# Fetch a ready job
job = actions.get_one_ready_job()

def main_loop():
    # If there is a ready job
    if (job):
        print(job.command)
        # Initiating an execution object
        job_execution = actions.create_job_execution(job, time.time(), 0 , 0, -1)

        # Mark job as running and dispatching the command
        actions.set_job_as_running(job)

        execution = run(job.command, shell=True)
        now_time = time.time()

        # if return status is 0
        if (execution.returncode==0):
            actions.update_job_execution(job_execution, now_time, (now_time - job_execution.start_time), 0)
            actions.set_job_as_completed(job)
            actions.update_next_ready_jobs(job)
        else:
            actions.update_job_execution(job_execution, now_time, (now_time - job_execution.start_time), execution.returncode)
            job.current_state = 'failed'
            actions.set_job_as_failed(job)

main_loop()