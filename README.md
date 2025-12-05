# 📊 Student Grade Tracker CLI

**Table of Contents**
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [File Descriptions](#file-descriptions)
- [Database Schema](#database-schema)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Student Grade Tracker is a command-line interface (CLI) application designed to help educators manage student records, courses, and grades. This application provides a simple yet powerful way to track academic performance, calculate GPAs, and generate reports—all from your terminal.

Built with Python, SQLAlchemy, and Alembic, this application demonstrates object-relational mapping (ORM), database management, and interactive CLI design principles.

## Features

✅ **Student Management**: Add, update, delete, and view student records

✅ **Course Management**: Create courses and assign students

✅ **Grade Tracking**: Record grades for assignments and calculate overall scores

✅ **GPA Calculation**: Automatically calculate student GPAs

✅ **Search & Filter**: Find students by name, course, or performance level

✅ **Data Persistence**: All data is stored in an SQLite database

✅ **User-Friendly Interface**: Intuitive menu system with clear prompts

✅ **Error Handling**: Robust input validation and error messages

## Installation

### Prerequisites
- Python 3.8 or higher
- pipenv (recommended) or pip

### Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/student-grade-tracker.git
   cd student-grade-tracker
   ```

2. **Set up virtual environment and dependencies**
   ```bash
   pipenv install
   pipenv shell
   ```

3. **Initialize the database**
   ```bash
   # Create and run migrations
   alembic upgrade head

   # Seed with sample data (optional)
   python lib/seed.py
   ```

4. **Run the application**
   ```bash
   python lib/cli.py
   ```

## Usage

### Starting the Application
```bash
python lib/cli.py
```

### Main Menu Options
```
=== STUDENT GRADE TRACKER ===
1. Manage Students
2. Manage Courses
3. Record Grades
4. View Reports
5. Calculate GPAs
0. Exit
===========================
>
```

### Example Workflow
- **Add a Student**: Navigate to "Manage Students" → "Add New Student"
- **Create a Course**: Navigate to "Manage Courses" → "Create New Course"
- **Enroll Student**: Navigate to "Manage Courses" → "Enroll Student in Course"
- **Record Grade**: Navigate to "Record Grades" → select student and course
- **View Report**: Navigate to "View Reports" → "Student Performance Report"

## Project Structure
```
.
├── Pipfile                    # Dependencies and virtual environment config
├── Pipfile.lock              # Locked dependency versions
├── README.md                 # This file
├── migrations/               # Alembic database migrations
│   ├── versions/
│   ├── env.py
│   └── alembic.ini
└── lib/                      # Main application code
    ├── __init__.py
    ├── cli.py               # Main CLI entry point
    ├── debug.py             # Debug utilities
    ├── helpers.py           # Helper functions
    ├── seed.py              # Database seeding script
    └── models/              # Database models
        ├── __init__.py      # Database configuration
        ├── student.py       # Student model
        ├── course.py        # Course model
        └── grade.py         # Grade model
```

## File Descriptions

### lib/cli.py - Main Application Entry Point
This is the heart of the CLI application. It contains the main menu loop and coordinates all user interactions.

**Key Functions:**
- `main()`: Entry point that displays the main menu and processes user choices
- `display_main_menu()`: Shows the primary navigation options

### lib/helpers.py - Utility Functions
Contains reusable helper functions for common operations.

**Key Functions:**
- `exit_program()`: Safely exits the application with proper cleanup
- `clear_screen()`: Clears the terminal for better readability
- `format_grade(score)`: Converts numerical scores to letter grades
- `calculate_gpa(student_id)`: Calculates GPA for a given student
- `validate_email(email)`: Validates email format
- `display_student_report(student)`: Generates formatted student reports

### lib/models/ - Database Models
Contains SQLAlchemy models that define the database schema.

#### models/__init__.py
Configures the database connection and session management.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database configuration
Base = declarative_base()
engine = create_engine('sqlite:///grades.db')
Session = sessionmaker(bind=engine)
session = Session()
```

#### models/student.py
Defines the Student model with relationships to courses and grades.

```python
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
```

#### models/course.py
Defines the Course model with course details and student relationships.

```python
class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)  # e.g., "CS101"
    name = Column(String, nullable=False)               # e.g., "Introduction to Programming"
    credits = Column(Integer, default=3)

    # Relationships
    grades = relationship("Grade", back_populates="course")
    students = relationship("Student", secondary=enrollments, back_populates="courses")
```

#### models/grade.py
Defines the Grade model linking students, courses, and scores.

```python
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
```

### lib/seed.py - Database Seeding
Populates the database with sample data for testing and demonstration.

**Key Functions:**
- `create_sample_students()`: Adds 10 sample students with realistic names
- `create_sample_courses()`: Creates common academic courses
- `enroll_students_in_courses()`: Randomly enrolls students in courses
- `add_sample_grades()`: Generates realistic grade distributions

### lib/debug.py - Debug Utilities
Contains functions for debugging database state and relationships.

**Key Functions:**
- `debug_all_students()`: Prints all students with their details
- `debug_student_grades(student_id)`: Shows grades for a specific student
- `debug_course_enrollment(course_id)`: Lists all students in a course

## Database Schema
```sql
-- Students Table
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    enrollment_date DATETIME
);

-- Courses Table
CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    credits INTEGER DEFAULT 3
);

-- Enrollments (Join Table)
CREATE TABLE enrollments (
    student_id INTEGER REFERENCES students(id),
    course_id INTEGER REFERENCES courses(id),
    enrollment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (student_id, course_id)
);

-- Grades Table
CREATE TABLE grades (
    id INTEGER PRIMARY KEY,
    student_id INTEGER REFERENCES students(id),
    course_id INTEGER REFERENCES courses(id),
    score REAL NOT NULL,
    assignment_name TEXT,
    date_recorded DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pipenv install --dev

# Run tests
pytest

# Check code style
flake8 lib/

# Run all tests and checks
./scripts/test_all.sh
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

**Quick Reference**

### Common Commands
```bash
# Run application
python lib/cli.py

# Create new migration
alembic revision --autogenerate -m"Add new feature"

# Apply migration
alembic upgrade head

# Seed database
python lib/seed.py

# Run debug utilities
python lib/debug.py
```

### GPA Scale (Default)
- A: 90-100 (4.0)
- B: 80-89 (3.0)
- C: 70-79 (2.0)
- D: 60-69 (1.0)
- F: 0-59 (0.0)

**Contact**
For questions or support, please open an issue on the GitHub repository.

*Built with ❤️ for Flatiron School's Phase 3 Project*