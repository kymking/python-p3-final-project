from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)  # e.g., "CS101"
    name = Column(String, nullable=False)               # e.g., "Introduction to Programming"
    credits = Column(Integer, default=3)

    # Relationships
    grades = relationship("Grade", back_populates="course")
    students = relationship("Student", secondary=enrollments, back_populates="courses")