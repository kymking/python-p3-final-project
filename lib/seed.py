#!/usr/bin/env python3
# lib/seed.py

from faker import Faker
from models import session, Student, Course, Grade, Base, engine
import random

fake = Faker()

def create_sample_students():
    """Adds sample students"""
    students_data = [
        ("John", "Smith", "john.smith@university.edu"),
        ("Emma", "Johnson", "emma.johnson@university.edu"),
        ("Michael", "Brown", "michael.brown@university.edu"),
        ("Sarah", "Davis", "sarah.davis@university.edu"),
        ("David", "Wilson", "david.wilson@university.edu"),
        ("Lisa", "Garcia", "lisa.garcia@university.edu"),
        ("James", "Miller", "james.miller@university.edu"),
        ("Jennifer", "Martinez", "jennifer.martinez@university.edu"),
        ("Robert", "Anderson", "robert.anderson@university.edu"),
        ("Maria", "Taylor", "maria.taylor@university.edu")
    ]

    for first, last, email in students_data:
        student = Student(first_name=first, last_name=last, email=email)
        session.add(student)

    session.commit()
    print("Sample students created.")


def create_sample_courses():
    """Creates common academic courses"""
    courses_data = [
        ("CS101", "Introduction to Programming", 3),
        ("MATH201", "Calculus II", 4),
        ("ENG102", "Composition", 3),
        ("HIST101", "World History", 3),
        ("BIO110", "Biology", 4),
        ("CHEM120", "Chemistry", 4),
        ("PHYS150", "Physics", 4),
        ("ECON200", "Microeconomics", 3)
    ]

    for code, name, credits in courses_data:
        course = Course(code=code, name=name, credits=credits)
        session.add(course)

    session.commit()
    print("Sample courses created.")


def enroll_students_in_courses():
    """Randomly enrolls students in courses"""
    students = session.query(Student).all()
    courses = session.query(Course).all()

    for student in students:
        # Each student enrolls in 3-5 random courses
        num_courses = random.randint(3, 5)
        selected_courses = random.sample(courses, num_courses)

        for course in selected_courses:
            if course not in student.courses:
                student.courses.append(course)

    session.commit()
    print("Students enrolled in courses.")


def add_sample_grades():
    """Generates realistic grade distributions"""
    students = session.query(Student).all()

    for student in students:
        for course in student.courses:
            # Generate 1-3 grades per course
            num_grades = random.randint(1, 3)

            for _ in range(num_grades):
                # Create a realistic grade distribution (bell curve around 75-85)
                base_score = random.gauss(80, 15)  # Mean 80, std dev 15
                score = max(0, min(100, base_score))  # Clamp to 0-100

                assignment_names = [
                    "Midterm Exam", "Final Exam", "Homework 1", "Homework 2",
                    "Project", "Quiz 1", "Quiz 2", "Lab Report", "Presentation"
                ]

                assignment_name = random.choice(assignment_names)

                grade = Grade(
                    student_id=student.id,
                    course_id=course.id,
                    score=round(score, 1),
                    assignment_name=assignment_name
                )
                session.add(grade)

    session.commit()
    print("Sample grades added.")


def seed_database():
    """Main seeding function"""
    print("Seeding database...")

    # Create tables if they don't exist
    Base.metadata.create_all(engine)

    # Clear existing data
    session.query(Grade).delete()
    session.query(Student).delete()
    session.query(Course).delete()
    session.commit()

    # Seed data
    create_sample_students()
    create_sample_courses()
    enroll_students_in_courses()
    add_sample_grades()

    print("Database seeded successfully!")


if __name__ == "__main__":
    seed_database()