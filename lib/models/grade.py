from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from . import Base

class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    score = Column(Float, nullable=False)  # 0-100 scale
    assignment_name = Column(String)
    date_recorded = Column(DateTime, default=datetime.now)

    # Relationships
    student = relationship("Student", back_populates="grades")
    course = relationship("Course", back_populates="grades")