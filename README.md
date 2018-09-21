# Pipe Line Monitor

A schduler to execute and run a pipe line of commands in a supercomputing facility. The program can schedule a graph-like execution sequence.

## Pre-requisites

```
- python 3.6
- sqlalchemy 1.2.7
- sqlite 3
- Linux/Unix (preferred)
```

## Database Models

```
Job
JobExecution
```

## Creating a pipeline
Always use the `create_pipeline.py` to add Jobs and link them to form the complete pipeline.
### Creating Jobs
```python
from pipeline.pipeline_actions import create_job

job_1 = create_job('<SHELL COMMAND>', <MEMORY>, <WALL TIME>, <CPUS>, '<MODULES', '<UNIQUE IDENTIFIER>')

job_2 = create_job('<SHELL COMMAND>', <MEMORY>, <WALL TIME>, <CPUS>, '<MODULES', '<UNIQUE IDENTIFIER>')

```
### Linking Jobs
Use the template `link_job_to_job(<PARENT JOB>, <CHILD JOB>)` to link.
```python
from pipeline.pipeline_actions import link_job_to_job

link_job_to_job(job_2, job_3)
```
## Pipeline Execution
Run the file `runner.py`, or submit the file to the Queue.
### Runner Functionality
It calls the method `main_loop()` everytime the file is executed. The steps within the method are as follows.

1. Fetch jobs in the `ready` state
2. Create an execution entry and dispatch the execution command
    * This adds and entry to the `jobs` table saying the its the current execution
    * Execution entry is added to `job_executions` table with the start time and a reference to the `jobs` table entry.
3. Actual execution
4. Record exit status (0 = success)
5. Remove the entry for current execution from `jobs` table
6. Update child jobs as ready
    * First obtain child jobs
    * Check if their parents have completed (To ensure multiple entries are satisfied)
    * Mark as `ready`

