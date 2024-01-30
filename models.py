from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship
from config import DB_URL


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
    department_id = Column(Integer)
    job_id = Column(Integer)


# Create the tables in the database
engine = create_engine(DB_URL)
Base.metadata.create_all(bind=engine)
