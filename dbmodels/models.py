from sqlalchemy import Column, Date, Integer, String, Text, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, mapper

engine = create_engine(
    'sqlite:////media/admin-u6776114/data/pipe-mgr/db/database.db', echo=True)
Base = declarative_base()

# job_association_table = Table('job_association', Base.metadata,
#                               Column('parent_job_id', Integer,
#                                      ForeignKey('jobs.id')),
#                               Column('child_job_id', Integer,
#                                      ForeignKey('jobs.id'))
#                               )


class job_association(Base):
    __tablename__ = 'job_association'
    id = Column(Integer, primary_key=True)
    child_job_id = Column(Integer, ForeignKey('jobs.id'))
    parent_job_id = Column(Integer, ForeignKey('jobs.id'))


class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    command = Column(Text)
    pipleine_id = Column(Integer, ForeignKey('pipelines.id'))
    required_memory = Column(Integer)
    required_wall_time = Column(Integer)
    required_cpus = Column(Integer)
    required_modules = Column(Text)
    unique = Column(Text)

    parents = relationship(
        'Job', secondary=job_association.__table__,
        primaryjoin='Job.id==job_association.child_job_id',
        secondaryjoin='job_association.parent_job_id==Job.id',
        backref="children")




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

    job_runs = relationship(
        "JobRun", backref=backref('pipeline_execution', remote_side=[id]))


class JobRun(Base):
    __tablename__ = 'job_runs'
    id = Column(Integer, primary_key=True)
    current_state = Column(Text)
    job_id = Column(Integer, ForeignKey('jobs.id'))
    pipeline_execution_id = Column(
        Integer, ForeignKey('pipeline_executions.id'))
    start_time = Column(Integer)
    end_time = Column(Integer)
    elapsed_time = Column(Integer)
    exit_status = Column(Integer)

# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     username = Column(String(256))
#     first_name = Column(String(256))
#     last_name = Column(String(256))
#     password = Column(String(256))


    # def __repr__(self):
    #     return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)
Base.metadata.create_all(engine)
# job = Job(command='sample command')
