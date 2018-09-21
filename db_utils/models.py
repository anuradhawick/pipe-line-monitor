import os
from sqlalchemy import Column, Date, Integer, String, Text, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, mapper
import db_utils.utils as utils

engine = utils.get_engine()

Base = declarative_base()


class job_association(Base):
    __tablename__ = 'job_association'
    id = Column(Integer, primary_key=True)
    child_job_id = Column(Integer, ForeignKey('jobs.id'))
    parent_job_id = Column(Integer, ForeignKey('jobs.id'))


class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    command = Column(Text)
    pipeline_id = Column(Integer, ForeignKey('pipelines.id'))
    current_execution_id = Column(Integer, ForeignKey('job_executions.id'))
    required_memory = Column(Integer)
    required_wall_time = Column(Integer)
    required_cpus = Column(Integer)
    current_state = Column(Text)  # ready, running, completed, failed
    required_modules = Column(Text)
    unique = Column(Text)

    parents = relationship(
        'Job', secondary=job_association.__table__,
        primaryjoin='Job.id==job_association.child_job_id',
        secondaryjoin='job_association.parent_job_id==Job.id',
        backref="children")

    current_execution = relationship(
        "JobExecution", uselist=False, foreign_keys="[Job.current_execution_id]")
    
    executions = relationship(
        "JobExecution", back_populates="job", foreign_keys="[JobExecution.job_id]")
    
    # TODO add relationship to pipeline


class JobExecution(Base):
    __tablename__ = 'job_executions'
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'))
    pipeline_execution_id = Column(
        Integer, ForeignKey('pipeline_executions.id'))
    start_time = Column(Integer)
    end_time = Column(Integer)
    elapsed_time = Column(Integer)
    exit_status = Column(Integer)

    job = relationship(
        "Job", back_populates="executions", foreign_keys="[JobExecution.job_id]")


class PipeLine(Base):
    __tablename__ = 'pipelines'
    id = Column(Integer, primary_key=True)
    pipeline_name = Column(Text)
    pipeline_owner = Column(Text)

    roots = relationship(
        "Job", backref=backref('pipeline', remote_side=[id]))

    executions = relationship(
        "PipeLineExecution", backref=backref('pipeline', remote_side=[id]))


class PipeLineExecution(Base):
    __tablename__ = 'pipeline_executions'
    id = Column(Integer, primary_key=True)
    pipeline_executor = Column(Text)
    start_time = Column(Integer)
    end_time = Column(Integer)
    elapsed_time = Column(Integer)
    pipeline_id = Column(Integer, ForeignKey('pipelines.id'))  

    job_executions = relationship(
        "JobExecution", backref=backref('pipeline_execution', remote_side=[id]))


Base.metadata.create_all(engine)
