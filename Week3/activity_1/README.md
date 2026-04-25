# Database Design for Student Enrollment System

## Project Overview
This repository contains the initial database design for a university enrollment system (Week 3 - Activity 1). The goal of this project is to design a normalized relational database schema that effectively manages students, courses, lecturers, and their complex relationships.

## Entity Relationship (ER) Diagram
The design follows the **Chen's Notation** for the conceptual model and is structured to be easily mapped to a physical relational database.

### Core Entities and Attributes

1.  **Students**:
    * `Student_id (PK)`: A unique identifier for each student.
    * `Student_name`: The full name of the student.
    * `Email`: Student's contact information.

2.  **Lecturer**:
    * `Lecturer_id (PK)`: A unique identifier for each lecturer.
    * `Lecturer_name`: The full name of the lecturer.
    * `Lecturer_description`: Background and expertise of the lecturer.
    * `Subjects`: Specialized areas of teaching.
    * `Email`: Lecturer's contact information.

3.  **Courses**:
    * `Course_id (PK)`: A unique identifier for each course.
    * `Course_name`: The title of the course.
    * `Location`: The classroom or platform where the course is held.
    * `Lecturer_id (FK)`: Links the course to its primary lecturer.

4.  **Enrollment (Junction Table)**:
    * `Enrollment_id (PK)`: Unique identifier for each enrollment record.
    * `Student_id (FK)`: References the student.
    * `Course_id (FK)`: References the course.
    * `Status`: Current status of the enrollment (e.g., Active, Completed).
    * `Memo`: Additional notes regarding the enrollment.

## Database Relationships

### 1. One-to-Many (1:N) Relationship: Lecturer and Courses
A single **Lecturer** can teach multiple **Courses**, but each course is typically assigned to one lecturer. This is implemented by placing the `Lecturer_id` as a **Foreign Key** in the `Courses` table.

### 2. Many-to-Many (M:N) Relationship: Students and Courses
The relationship between **Students** and **Courses** is Many-to-Many, as a student can enroll in multiple courses, and each course can host many students. 
* To resolve this, a junction table named **Enrollment** was created.
* This table breaks down the M:N relationship into two 1:N relationships, ensuring data integrity and allowing for additional attributes like `Status`.

## Conclusion
The design adheres to the principles of database normalization, ensuring that there is no data redundancy and that all foreign keys are placed in the "Many" side of relationships to maintain the atomic nature of the fields.