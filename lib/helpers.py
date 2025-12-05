# lib/helpers.py

import os
from models import session, Student, Course, Grade
from sqlalchemy.exc import IntegrityError


def exit_program():
    """Safely exits the application with proper cleanup"""
    print("Goodbye!")
    session.close()
    exit()


def clear_screen():
    """Clears the terminal for better readability"""
    os.system('cls' if os.name == 'nt' else 'clear')


def format_grade(score):
    """Converts numerical scores to letter grades"""
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'


def calculate_gpa(student_id):
    """Calculates GPA for a given student"""
    grades = session.query(Grade).filter_by(student_id=student_id).all()
    if not grades:
        return 0.0

    total_points = 0
    total_credits = 0

    for grade in grades:
        letter = format_grade(grade.score)
        points = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}[letter]
        total_points += points * grade.course.credits
        total_credits += grade.course.credits

    return total_points / total_credits if total_credits > 0 else 0.0


def validate_email(email):
    """Validates email format"""
    return '@' in email and '.' in email


def display_student_report(student):
    """Generates formatted student reports"""
    print(f"\nSTUDENT REPORT: {student.first_name} {student.last_name} (ID: {student.id})")
    print("-" * 50)
    print(f"Email: {student.email}")
    print(f"Enrollment Date: {student.enrollment_date.strftime('%Y-%m-%d') if student.enrollment_date else 'N/A'}")

    grades = session.query(Grade).filter_by(student_id=student.id).all()
    if grades:
        print("\nCOURSES & GRADES:")
        for grade in grades:
            letter = format_grade(grade.score)
            print(f"• {grade.course.code}: {grade.course.name} - {letter} ({grade.score:.1f}%)")
        gpa = calculate_gpa(student.id)
        print(f"\nOVERALL GPA: {gpa:.2f}")
        print(f"STATUS: {'Good Standing' if gpa >= 2.0 else 'Academic Probation'}")
    else:
        print("\nNo grades recorded yet.")


# Student Management Functions
def manage_students():
    """Student management submenu"""
    while True:
        print("\n=== STUDENT MANAGEMENT ===")
        print("1. List All Students")
        print("2. Add New Student")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Back to Main Menu")

        choice = input("> ")

        if choice == "1":
            list_students()
        elif choice == "2":
            add_student()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            break
        else:
            print("Invalid choice")


def list_students():
    """Lists all students"""
    students = session.query(Student).all()
    if not students:
        print("No students found.")
        return

    print("\nALL STUDENTS:")
    print("-" * 50)
    for student in students:
        print(f"ID: {student.id} | {student.first_name} {student.last_name} | {student.email}")


def add_student():
    """Adds a new student"""
    print("\nADD NEW STUDENT")
    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    email = input("Email: ").strip()

    if not all([first_name, last_name, email]):
        print("All fields are required.")
        return

    if not validate_email(email):
        print("Invalid email format.")
        return

    try:
        student = Student(first_name=first_name, last_name=last_name, email=email)
        session.add(student)
        session.commit()
        print(f"Student {first_name} {last_name} added successfully!")
    except IntegrityError:
        session.rollback()
        print("Email already exists.")


def search_student():
    """Searches for a student by name or email"""
    query = input("Enter student name or email to search: ").strip()
    students = session.query(Student).filter(
        (Student.first_name.ilike(f'%{query}%')) |
        (Student.last_name.ilike(f'%{query}%')) |
        (Student.email.ilike(f'%{query}%'))
    ).all()

    if not students:
        print("No students found.")
        return

    print("\nSEARCH RESULTS:")
    for student in students:
        print(f"ID: {student.id} | {student.first_name} {student.last_name} | {student.email}")


def update_student():
    """Updates student information"""
    student_id = input("Enter student ID to update: ").strip()
    try:
        student_id = int(student_id)
    except ValueError:
        print("Invalid ID.")
        return

    student = session.query(Student).get(student_id)
    if not student:
        print("Student not found.")
        return

    print(f"Current: {student.first_name} {student.last_name} | {student.email}")
    first_name = input("New First Name (leave blank to keep current): ").strip() or student.first_name
    last_name = input("New Last Name (leave blank to keep current): ").strip() or student.last_name
    email = input("New Email (leave blank to keep current): ").strip() or student.email

    if not validate_email(email):
        print("Invalid email format.")
        return

    try:
        student.first_name = first_name
        student.last_name = last_name
        student.email = email
        session.commit()
        print("Student updated successfully!")
    except IntegrityError:
        session.rollback()
        print("Email already exists.")


def delete_student():
    """Deletes a student"""
    student_id = input("Enter student ID to delete: ").strip()
    try:
        student_id = int(student_id)
    except ValueError:
        print("Invalid ID.")
        return

    student = session.query(Student).get(student_id)
    if not student:
        print("Student not found.")
        return

    confirm = input(f"Are you sure you want to delete {student.first_name} {student.last_name}? (y/n): ").lower()
    if confirm == 'y':
        session.delete(student)
        session.commit()
        print("Student deleted successfully!")
    else:
        print("Deletion cancelled.")


# Course Management Functions
def manage_courses():
    """Course management submenu"""
    while True:
        print("\n=== COURSE MANAGEMENT ===")
        print("1. List All Courses")
        print("2. Create New Course")
        print("3. Enroll Student in Course")
        print("4. View Course Enrollment")
        print("5. Back to Main Menu")

        choice = input("> ")

        if choice == "1":
            list_courses()
        elif choice == "2":
            create_course()
        elif choice == "3":
            enroll_student()
        elif choice == "4":
            view_course_enrollment()
        elif choice == "5":
            break
        else:
            print("Invalid choice")


def list_courses():
    """Lists all courses"""
    courses = session.query(Course).all()
    if not courses:
        print("No courses found.")
        return

    print("\nALL COURSES:")
    print("-" * 50)
    for course in courses:
        print(f"{course.code}: {course.name} ({course.credits} credits)")


def create_course():
    """Creates a new course"""
    print("\nCREATE NEW COURSE")
    code = input("Course Code (e.g., CS101): ").strip().upper()
    name = input("Course Name: ").strip()
    credits = input("Credits: ").strip()

    if not all([code, name, credits]):
        print("All fields are required.")
        return

    try:
        credits = int(credits)
    except ValueError:
        print("Credits must be a number.")
        return

    try:
        course = Course(code=code, name=name, credits=credits)
        session.add(course)
        session.commit()
        print(f"Course {code} created successfully!")
    except IntegrityError:
        session.rollback()
        print("Course code already exists.")


def enroll_student():
    """Enrolls a student in a course"""
    student_id = input("Enter student ID: ").strip()
    course_code = input("Enter course code: ").strip().upper()

    try:
        student_id = int(student_id)
    except ValueError:
        print("Invalid student ID.")
        return

    student = session.query(Student).get(student_id)
    if not student:
        print("Student not found.")
        return

    course = session.query(Course).filter_by(code=course_code).first()
    if not course:
        print("Course not found.")
        return

    if course in student.courses:
        print("Student is already enrolled in this course.")
        return

    student.courses.append(course)
    session.commit()
    print(f"Student {student.first_name} {student.last_name} enrolled in {course.code} successfully!")


def view_course_enrollment():
    """Views enrollment for a specific course"""
    course_code = input("Enter course code: ").strip().upper()
    course = session.query(Course).filter_by(code=course_code).first()

    if not course:
        print("Course not found.")
        return

    print(f"\nENROLLMENT FOR {course.code}: {course.name}")
    print("-" * 50)

    if not course.students:
        print("No students enrolled.")
        return

    for student in course.students:
        print(f"ID: {student.id} | {student.first_name} {student.last_name}")


# Grade Recording Functions
def record_grades():
    """Records grades for students"""
    student_id = input("Enter student ID: ").strip()
    course_code = input("Enter course code: ").strip().upper()

    try:
        student_id = int(student_id)
    except ValueError:
        print("Invalid student ID.")
        return

    student = session.query(Student).get(student_id)
    if not student:
        print("Student not found.")
        return

    course = session.query(Course).filter_by(code=course_code).first()
    if not course:
        print("Course not found.")
        return

    if course not in student.courses:
        print("Student is not enrolled in this course.")
        return

    score = input("Enter score (0-100): ").strip()
    assignment_name = input("Assignment name (optional): ").strip()

    try:
        score = float(score)
        if not 0 <= score <= 100:
            raise ValueError
    except ValueError:
        print("Score must be a number between 0 and 100.")
        return

    grade = Grade(student_id=student_id, course_id=course.id, score=score, assignment_name=assignment_name or None)
    session.add(grade)
    session.commit()
    print(f"Grade recorded: {format_grade(score)} ({score:.1f}%) for {student.first_name} {student.last_name} in {course.code}")


# Report Functions
def view_reports():
    """Views various reports"""
    while True:
        print("\n=== VIEW REPORTS ===")
        print("1. Student Performance Report")
        print("2. Course Grade Report")
        print("3. Back to Main Menu")

        choice = input("> ")

        if choice == "1":
            student_performance_report()
        elif choice == "2":
            course_grade_report()
        elif choice == "3":
            break
        else:
            print("Invalid choice")


def student_performance_report():
    """Shows detailed student performance"""
    student_id = input("Enter student ID: ").strip()
    try:
        student_id = int(student_id)
    except ValueError:
        print("Invalid ID.")
        return

    student = session.query(Student).get(student_id)
    if not student:
        print("Student not found.")
        return

    display_student_report(student)


def course_grade_report():
    """Shows grades for a specific course"""
    course_code = input("Enter course code: ").strip().upper()
    course = session.query(Course).filter_by(code=course_code).first()

    if not course:
        print("Course not found.")
        return

    grades = session.query(Grade).filter_by(course_id=course.id).all()
    if not grades:
        print("No grades recorded for this course.")
        return

    print(f"\nGRADES FOR {course.code}: {course.name}")
    print("-" * 60)
    print("Student Name".ljust(20) + "Score".ljust(8) + "Grade".ljust(6) + "Assignment")
    print("-" * 60)

    for grade in grades:
        student_name = f"{grade.student.first_name} {grade.student.last_name}"
        score = f"{grade.score:.1f}%"
        letter = format_grade(grade.score)
        assignment = grade.assignment_name or "N/A"
        print(f"{student_name[:19].ljust(20)}{score.ljust(8)}{letter.ljust(6)}{assignment}")


# GPA Functions
def calculate_gpas():
    """Calculates and displays GPAs"""
    while True:
        print("\n=== CALCULATE GPAS ===")
        print("1. Calculate GPA for Specific Student")
        print("2. Show All Students GPAs")
        print("3. Back to Main Menu")

        choice = input("> ")

        if choice == "1":
            specific_student_gpa()
        elif choice == "2":
            all_students_gpa()
        elif choice == "3":
            break
        else:
            print("Invalid choice")


def specific_student_gpa():
    """Calculates GPA for a specific student"""
    student_id = input("Enter student ID: ").strip()
    try:
        student_id = int(student_id)
    except ValueError:
        print("Invalid ID.")
        return

    student = session.query(Student).get(student_id)
    if not student:
        print("Student not found.")
        return

    gpa = calculate_gpa(student_id)
    print(f"\nGPA for {student.first_name} {student.last_name}: {gpa:.2f}")


def all_students_gpa():
    """Shows GPAs for all students"""
    students = session.query(Student).all()
    if not students:
        print("No students found.")
        return

    print("\nALL STUDENTS GPAs:")
    print("-" * 40)
    print("Student Name".ljust(25) + "GPA")
    print("-" * 40)

    for student in students:
        gpa = calculate_gpa(student.id)
        student_name = f"{student.first_name} {student.last_name}"
        print(f"{student_name[:24].ljust(25)}{gpa:.2f}")
