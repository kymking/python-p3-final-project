from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from . import Base

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    enrollment_date = Column(DateTime, default=datetime.now)

    # Relationships
    grades = relationship("Grade", back_populates="student", cascade="all, delete-orphan")
    courses = relationship("Course", secondary=enrollments, back_populates="students")