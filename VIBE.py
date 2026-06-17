#Zakaria Nabulsi
#CIS261
#WK10 VIBE Coding - Student Grade Calculator


"""Student Grade Calculator.

This program manages student records, calculates average scores and letter grades,
and allows the user to display class statistics and search for students.
"""

from typing import List, Dict

FILE_NAME = "student_grades.txt"


# ------------------------------
# Helper functions
# ------------------------------
def calculate_average(test1: float, test2: float, test3: float) -> float:
    """Return the average of three test scores."""
    return (test1 + test2 + test3) / 3


def determine_grade(average: float) -> str:
    """Return the letter grade for the given average."""
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"


def format_score(value: float) -> str:
    """Format a numeric score to two decimal places."""
    return f"{value:.2f}"


def prompt_float(prompt: str) -> float:
    """Prompt for a floating-point value until a valid number is entered."""
    while True:
        user_input = input(prompt).strip()
        if user_input.upper() == "ESC":
            raise KeyboardInterrupt
        try:
            return float(user_input)
        except ValueError:
            print("Please enter a valid number.")


# ------------------------------
# File functions
# ------------------------------
def load_students() -> List[Dict[str, object]]:
    """Load student records from the file if it exists."""
    students: List[Dict[str, object]] = []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                raw_line = line.strip()
                if not raw_line:
                    continue

                parts = raw_line.split("|")
                if len(parts) != 7:
                    print(f"Warning: Skipping malformed line {line_number} in {FILE_NAME}.")
                    continue

                name, student_id, test1, test2, test3, average, grade = parts
                try:
                    students.append(
                        {
                            "name": name,
                            "id": student_id,
                            "test1": float(test1),
                            "test2": float(test2),
                            "test3": float(test3),
                            "average": float(average),
                            "grade": grade,
                        }
                    )
                except ValueError:
                    print(f"Warning: Skipping invalid numeric data on line {line_number}.")
    except FileNotFoundError:
        print(f"{FILE_NAME} not found. Starting with an empty list.")
    except OSError as error:
        print(f"Error reading {FILE_NAME}: {error}")

    if students:
        print(f"Loaded {len(students)} student record(s) from {FILE_NAME}.")
    else:
        print(f"No records found in {FILE_NAME}.")
    return students


def save_students(students: List[Dict[str, object]]) -> None:
    """Save all student records to the pipe-delimited file."""
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            for student in students:
                file.write(
                    f"{student['name']}|{student['id']}|"
                    f"{student['test1']:.2f}|{student['test2']:.2f}|"
                    f"{student['test3']:.2f}|{student['average']:.2f}|"
                    f"{student['grade']}\n"
                )
        print(f"Records saved successfully to {FILE_NAME}.")
    except OSError as error:
        print(f"Error saving to {FILE_NAME}: {error}")


# ------------------------------
# Student actions
# ------------------------------
def add_student(students: List[Dict[str, object]]) -> None:
    """Prompt the user to add one student and save the result."""
    try:
        name = input("Enter student name: ").strip()
        if name.upper() == "ESC":
            print("Returning to menu.")
            return
        if not name:
            print("Student name cannot be blank.")
            return

        student_id = input("Enter student ID: ").strip()
        if student_id.upper() == "ESC":
            print("Returning to menu.")
            return
        if not student_id:
            print("Student ID cannot be blank.")
            return

        test1 = prompt_float("Enter Test 1 score: ")
        test2 = prompt_float("Enter Test 2 score: ")
        test3 = prompt_float("Enter Test 3 score: ")
    except KeyboardInterrupt:
        print("\nReturning to menu.")
        return

    average = calculate_average(test1, test2, test3)
    grade = determine_grade(average)

    student = {
        "name": name,
        "id": student_id,
        "test1": test1,
        "test2": test2,
        "test3": test3,
        "average": average,
        "grade": grade,
    }

    students.append(student)
    save_students(students)
    print(f"Student {name} added successfully.\n")


def display_students(students: List[Dict[str, object]]) -> None:
    """Display all student records in a formatted table."""
    if not students:
        print("No student records to display.")
        return

    print("\nStudent Records")
    print("-" * 110)
    print(
        f"{'Name':<15} {'ID':<10} {'Test 1':>8} {'Test 2':>8} {'Test 3':>8} "
        f"{'Average':>9} {'Grade':>6}"
    )
    print("-" * 110)

    for student in students:
        print(
            f"{student['name']:<15} {student['id']:<10} "
            f"{student['test1']:>8.2f} {student['test2']:>8.2f} {student['test3']:>8.2f} "
            f"{student['average']:>9.2f} {student['grade']:>6}"
        )
    print("-" * 110)


def display_statistics(students: List[Dict[str, object]]) -> None:
    """Display class statistics."""
    if not students:
        print("No student records available for statistics.")
        return

    averages = [student["average"] for student in students]
    highest = max(averages)
    lowest = min(averages)
    class_average = sum(averages) / len(averages)

    print("\nClass Statistics")
    print("-" * 40)
    print(f"Highest Average: {highest:.2f}")
    print(f"Lowest Average:  {lowest:.2f}")
    print(f"Class Average:   {class_average:.2f}")
    print("-" * 40)


def search_student(students: List[Dict[str, object]]) -> None:
    """Search for a student by name, case-insensitive."""
    search_name = input("Enter the student name to search: ").strip()
    if search_name.upper() == "ESC":
        print("Returning to menu.")
        return

    search_query = search_name.lower()
    matches = [student for student in students if search_query in student["name"].lower()]

    if not matches:
        print("No matching student found.")
        return

    print("\nMatching Students")
    print("-" * 110)
    for student in matches:
        print(
            f"{student['name']:<15} {student['id']:<10} "
            f"{student['test1']:>8.2f} {student['test2']:>8.2f} {student['test3']:>8.2f} "
            f"{student['average']:>9.2f} {student['grade']:>6}"
        )
    print("-" * 110)


# ------------------------------
# Menu
# ------------------------------
def show_menu() -> None:
    """Display the main menu."""
    print("\nStudent Grade Calculator")
    print("1. Add Student")
    print("2. Display All Students")
    print("3. Display Class Statistics")
    print("4. Search Student by Name")
    print("5. Save Records")
    print("6. Exit")
    print("Type ESC at any time to exit.")


def main() -> None:
    """Run the main program loop."""
    students = load_students()

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice.upper() == "ESC":
            print("Exiting program. Goodbye!")
            break
        elif choice == "1":
            add_student(students)
        elif choice == "2":
            display_students(students)
        elif choice == "3":
            display_statistics(students)
        elif choice == "4":
            search_student(students)
        elif choice == "5":
            save_students(students)
        elif choice == "6":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid selection. Please choose 1-6 or ESC.")


if __name__ == "__main__":
    main()
