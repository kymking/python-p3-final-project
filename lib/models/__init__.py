from sqlalchemy import create_engine, Table, Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

# Database configuration
Base = declarative_base()
engine = create_engine('sqlite:///grades.db')
Session = sessionmaker(bind=engine)
session = Session()

# Association table for many-to-many relationship between students and courses
enrollments = Table(
    'enrollments',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id'), primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True),
    Column('enrollment_date', DateTime, default=datetime.now)
)

# Import models to register them with Base
from .student import Student
from .course import Course
from .grade import Grade
