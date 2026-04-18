class Student:
    # A class to represent a student with name, age, and student ID.

    def __init__(self, name, age, student_id):
        self.name = name
        self.age = age
        self.student_id = student_id


def collect_students():
    # Collect data for a given number of students.
    students = []
    for i in range(3):
        print(f"Enter details for student {i+1}:")
        name = input("Name: ")
        age = int(input("Age: "))
        student_id = input("Student ID: ")
        student = Student(name, age, student_id)
        students.append(student)
    return students


def print_students(students):
    #Print the list of student names and ages in alphabetical order by name.
    # Sort students by name
    sorted_students = sorted(students, key=lambda s: s.name)
    print("\nList of students (sorted by name):")
    for student in sorted_students:
        print(f"Name: {student.name}, Age: {student.age}")


if __name__ == "__main__":
    # Collect data for at least 3 students
    students = collect_students()
    print_students(students)