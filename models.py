from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    department = Column(String)


class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    job = Column(String)


class HiredEmployees(Base):
    __tablename__ = 'hired_employees'
    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    name = Column(String)
    hire_datetime = Column(DateTime)
    department_id = Column(Integer, ForeignKey('departments.id'))
    job_id = Column(Integer, ForeignKey('jobs.id'))


# Create the tables in the database
DATABASE_URL = "postgresql://postgres:postgres@localhost/data"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)