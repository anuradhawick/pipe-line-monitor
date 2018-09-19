from pipeline.runner_actions import getOneReadyJob

# Fetch ready jobs
job = getOneReadyJob()
if (job):
    print(job.command)
