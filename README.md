# Lab4-NaelHaidar_IhabFaour
**School Management System project combining Tkinter and PyQt documented implementations**

## Project Description: School Management System

The School Management System (SMS) is a desktop application designed to facilitate the management of student and instructor information, courses, and related operations within an educational institution. The application aims to streamline administrative tasks and enhance user interaction through graphical user interfaces (GUIs) developed with Tkinter and PyQt5.

### Key Features
- **User Management**: Register and manage students and instructors.
- **Course Management**: Create, update, and manage courses offered by the institution.
- **Database Integration**: 
  - Store and retrieve data using **MySQL** for the Tkinter implementation.
  - Store and retrieve data using **SQLite** for the PyQt5 implementation.
- **Data Validation**: Validate user inputs to maintain data integrity.
- **User Interface**: User-friendly GUIs for seamless navigation and interaction.

## Class Structures

### Person Class

#### Attributes:
- `name`: The name of the person.
- `age`: The age of the person.
- `email`: The email address.

#### Methods:
- Validation and serialization methods to ensure proper data handling.

### Student Class (Inherits from Person)

#### Attributes:
- `student_id`: Unique identifier for each student.
- `enrolled_courses`: A list of courses that the student is enrolled in.

#### Methods:
- Methods for enrolling in and withdrawing from courses.
- Override methods for validation and serialization.

### Instructor Class (Inherits from Person)

#### Attributes:
- `instructor_id`: Unique identifier for each instructor.
- `assigned_courses`: A list of courses taught by the instructor.

#### Methods:
- Methods for assigning and unassigning courses.
- Override methods for validation and serialization.

### Course Class

#### Attributes:
- `course_id`: Unique identifier for each course.
- `course_name`: Name of the course.
- `credits`: Number of credits assigned to the course.

#### Methods:
- Methods to add students, remove students, and manage course details.

## Database Interaction

### MySQL with Tkinter
The Tkinter implementation uses MySQL to handle database operations, ensuring data persistence and allowing for efficient storage and retrieval of information related to students, instructors, and courses. The integration with MySQL is managed using the `mysql-connector-python` library.

### SQLite with PyQt
The PyQt5 implementation uses SQLite, managed through SQLAlchemy, for database operations. This ensures efficient storage and retrieval of data while maintaining consistency and accessibility.

## User Interface

### PyQt5 GUI
The application employs a PyQt5 GUI that includes various widgets such as:
- `QLabel`: For displaying text.
- `QLineEdit`: For user input.
- `QPushButton`: For triggering actions.
- `QComboBox`: For selecting options.
- `QTableWidget`: For displaying lists of students, instructors, and courses.

### Tkinter GUI
The Tkinter GUI includes widgets such as:
- `Label`: For displaying text.
- `Entry`: For user input.
- `Button`: For triggering actions.
- `Combobox`: For selecting options.
- `Treeview`: For displaying lists of students, instructors, and courses.

## File Structure

- `Lab2.py`: Contains the definitions of the Person, Student, Instructor, and Course classes.
- `Part2_GUI.py`: Contains the initialization of Tkinter GUI and connect with MySQL database. 
- `PyQt5.py`: Contains the initialization of PyQT GUI and connect with SQlite database
- `docs directory`: Contains the html source code of the sphinx documentation

## How to Run the Application

### Prerequisites
- Python 3.x installed on your machine.
- Required Python libraries: PyQt5, Tkinter, SQLAlchemy, mysql-connector-python, and SQLite.

### Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <path>
   ```

2. **Install Required Libraries**
   ```bash
   pip install pyqt5 sqlalchemy mysql-connector-python
   ```

3. **Database Setup**

   - **For MySQL (Tkinter)**:
     - Create a MySQL database.
     - Update the `Part2_GUI.py` file with your MySQL connection details.

   - **For SQLite (PyQt5)**:
     - The SQLite database is automatically created when you run the application.

### Running the Application

1. **Tkinter Implementation (MySQL)**
   ```bash
   python Part2_GUI.py
   ```

2. **PyQt5 Implementation (SQLite)**
   ```bash
   python PyQt5.py
   ```

### Interacting with the Databases

- **Tkinter (MySQL)**:
  - You can manage users, courses, registration, delete, edit, load data, and other entities through the Tkinter interface. Data will be stored and retrieved from the MySQL database.

- **PyQt5 (SQLite)**:
  - You can manage users, courses, and other entities through the PyQt5 interface. Data will be stored and retrieved from the SQLite database.


## Database Initialization Scripts

To set up the MySQL database for the School Management System, run the following SQL scripts:

### Create Database and Tables

```sql
-- Create database
CREATE DATABASE school_management_system;

-- Use the database
USE school_management_system;

-- Create students table
CREATE TABLE students (
    student_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Create instructors table
CREATE TABLE instructors (
    instructor_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Create courses table
CREATE TABLE courses (
    course_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    instructor_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (instructor_name) REFERENCES instructors(name)
    ON UPDATE CASCADE 
    ON DELETE CASCADE
);

-- Create course_registrations table
CREATE TABLE course_registrations (
    student_name VARCHAR(255),
    course_name VARCHAR(255),
    FOREIGN KEY (student_name) REFERENCES students(name),
    FOREIGN KEY (course_name) REFERENCES courses(name)
);
```

### Modify Foreign Key Constraints

```sql
ALTER TABLE courses
DROP FOREIGN KEY fk_instructor_name;

ALTER TABLE courses
ADD CONSTRAINT fk_instructor_name
FOREIGN KEY (instructor_name) 
REFERENCES instructors(name) 
ON UPDATE CASCADE 
ON DELETE CASCADE;
```

These scripts create the necessary database and tables for the School Management System. Run these commands in your MySQL environment to set up the database before starting the application.

## Conclusion

This School Management System project provides a comprehensive solution for managing educational data, enhancing operational efficiency, and ensuring ease of use for administrators, students, and instructors. The class structures and integration with different databases form the backbone of the application, enabling smooth functionality and data management.

Feel free to explore and contribute to the project!
