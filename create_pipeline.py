from pipeline.pipeline_actions import create_job, link_job_to_job, set_job_as_ready

# creating a job
job_1 = create_job('sleep "5"', 123, 123,
                  345, 'modules')

job_2 = create_job('sleep "10"', 1323,
                  1233, 3453, 'modules')

job_3 = create_job('sleep "30"', 1323,
                  1233, 3453, 'modules')

job_4 = create_job('sleep "35"', 1323,
                  1233, 3453, 'modules')



# linking jobs
# job 1 is the root 
link_job_to_job(parent_job=job_1, child_job=job_2)
set_job_as_ready([job_1])
# job 2 is the parent for jobs 3, 4
link_job_to_job(parent_job=job_2, child_job=job_3)
link_job_to_job(parent_job=job_2, child_job=job_4)
