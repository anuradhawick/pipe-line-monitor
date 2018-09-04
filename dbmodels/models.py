from sqlalchemy import Column, Date, Integer, String, Text, ForeignKey, create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

engine = create_engine(
    'sqlite:////media/admin-u6776114/data/pipe-mgr/db/database.db', echo=True)
Base = declarative_base()

association_table = Table('job_association', Base.metadata,
    Column('parent_job_id', Integer, ForeignKey('jobs.id')),
    Column('child_job_id', Integer, ForeignKey('jobs.id'))
)

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    command = Column(Text)
    pipleine_id = Column(Integer, ForeignKey('pipelines.id'))
    required_memory = Column(Integer)
    required_wall_time = Column(Integer)
    required_cpus = Column(Integer)
    current_state = Column(Text)
    job_id = Column(Integer)
    start_time = Column(Integer)
    end_time = Column(Integer)
    elapsed_time = Column(Integer)
    exit_status = Column(Integer)
    required_modules = Column(Text)
    unique = Column(Text)

    children = relationship(
        "Job",
        secondary=association_table,
        back_populates="parents")
    
    parents = relationship(
        "Job",
        secondary=association_table,
        back_populates="children")


class PipeLine(Base):
    __tablename__ = 'pipelines'
    id = Column(Integer, primary_key=True)
    pipeline_name = Column(Text)
    pipeline = Column(Text)
    
    roots = relationship(
        "Job", backref=backref('pipeline', remote_side=[id]))


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(256))
    first_name = Column(String(256))
    last_name = Column(String(256))
    password = Column(String(256))


    # def __repr__(self):
    #     return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)
Base.metadata.create_all(engine)
# job = Job(command='sample command')
