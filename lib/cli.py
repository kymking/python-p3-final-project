# lib/cli.py

from helpers import *


def main():
    """Main application loop"""
    while True:
        display_main_menu()
        choice = input("> ")

        if choice == "0":
            exit_program()
        elif choice == "1":
            manage_students()
        elif choice == "2":
            manage_courses()
        elif choice == "3":
            record_grades()
        elif choice == "4":
            view_reports()
        elif choice == "5":
            calculate_gpas()
        else:
            print("Invalid choice")


def display_main_menu():
    """Shows the primary navigation options"""
    print("=== STUDENT GRADE TRACKER ===")
    print("1. Manage Students")
    print("2. Manage Courses")
    print("3. Record Grades")
    print("4. View Reports")
    print("5. Calculate GPAs")
    print("0. Exit")
    print("===========================")


if __name__ == "__main__":
    main()
