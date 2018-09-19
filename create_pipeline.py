from pipeline.pipeline_actions import createJob, linkJobToJob, setJobAsReady

# creating a job
job_1 = createJob('sleep 5 && echo "slept 5"', 123, 123,
                  345, 'modules', 'unique something')

job_2 = createJob('sleep 10 && echo "slept 10"', 1323,
                  1233, 3453, 'modules', 'unique something')

job_3 = createJob('sleep 30 && echo "slept 30"', 1323,
                  1233, 3453, 'modules', 'unique something')

job_4 = createJob('sleep 35 && echo "slept 35"', 1323,
                  1233, 3453, 'modules', 'unique something')



# linking jobs
# job 1 is the root 
linkJobToJob(job_1, job_2)
setJobAsReady(job_1)
# job 2 is the parent for jobs 3, 4
linkJobToJob(job_2, job_3)
linkJobToJob(job_2, job_4)
