#!/usr/bin/env python3
# lib/debug.py

from models import session, Student, Course, Grade
import ipdb


def debug_all_students():
    """Prints all students with their details"""
    students = session.query(Student).all()
    print(f"\n=== ALL STUDENTS ({len(students)}) ===")
    for student in students:
        print(f"ID: {student.id} | {student.first_name} {student.last_name} | {student.email}")
        print(f"  Courses: {[course.code for course in student.courses]}")
        print(f"  Grades: {len(student.grades)}")


def debug_student_grades(student_id):
    """Shows grades for a specific student"""
    student = session.query(Student).get(student_id)
    if not student:
        print("Student not found.")
        return

    print(f"\n=== GRADES FOR {student.first_name} {student.last_name} ===")
    for grade in student.grades:
        print(f"{grade.course.code}: {grade.score:.1f}% ({grade.assignment_name})")


def debug_course_enrollment(course_code):
    """Lists all students in a course"""
    course = session.query(Course).filter_by(code=course_code).first()
    if not course:
        print("Course not found.")
        return

    print(f"\n=== ENROLLMENT FOR {course.code}: {course.name} ===")
    for student in course.students:
        print(f"ID: {student.id} | {student.first_name} {student.last_name}")


def debug_all_grades():
    """Shows all grades in the system"""
    grades = session.query(Grade).all()
    print(f"\n=== ALL GRADES ({len(grades)}) ===")
    for grade in grades:
        student_name = f"{grade.student.first_name} {grade.student.last_name}"
        print(f"{student_name} - {grade.course.code}: {grade.score:.1f}% ({grade.assignment_name})")


def debug_database_stats():
    """Shows database statistics"""
    student_count = session.query(Student).count()
    course_count = session.query(Course).count()
    grade_count = session.query(Grade).count()

    print("\n=== DATABASE STATISTICS ===")
    print(f"Students: {student_count}")
    print(f"Courses: {course_count}")
    print(f"Grades: {grade_count}")


if __name__ == "__main__":
    print("Debug utilities loaded. Use functions like debug_all_students(), debug_student_grades(1), etc.")
    ipdb.set_trace()
