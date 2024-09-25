# Lab4-NaelHaidar_IhabFaour
School Management System project combining Tkinter and PyQt documented implementations
Project Description: School Management System
The School Management System (SMS) is a desktop application designed to facilitate the management of student and instructor information, courses, and related operations within an educational institution. The application aims to streamline administrative tasks and enhance user interaction through a graphical user interface (GUI) developed with PyQt5.

Key Features:
User Management: Register and manage students and instructors.
Course Management: Create, update, and manage courses offered by the institution.
Database Integration: Store and retrieve data using SQLite, ensuring persistence of information across sessions.
Data Validation: Validate user inputs to maintain data integrity.
User Interface: A user-friendly GUI for seamless navigation and interaction.
Class Structures
The following classes are defined in the project to represent different entities and functionalities:

Person Class

Attributes:
name: The name of the person.
age: The age of the person.
email: The email address.
Methods:
Validation and serialization methods to ensure proper data handling.
Student Class (Inherits from Person)

Attributes:
student_id: Unique identifier for each student.
enrolled_courses: A list of courses that the student is enrolled in.
Methods:
Methods for enrolling in and withdrawing from courses.
Override methods for validation and serialization.
Instructor Class (Inherits from Person)

Attributes:
instructor_id: Unique identifier for each instructor.
assigned_courses: A list of courses taught by the instructor.
Methods:
Methods for assigning and unassigning courses.
Override methods for validation and serialization.
Course Class

Attributes:
course_id: Unique identifier for each course.
course_name: Name of the course.
credits: Number of credits assigned to the course.
Methods:
Methods to add students, remove students, and manage course details.
Database Interaction
The project integrates SQLite using SQLAlchemy to handle database operations, allowing for efficient storage and retrieval of data related to students, instructors, and courses. This structure ensures that data remains consistent and accessible.
User Interface
The application employs a PyQt5 GUI that includes various widgets such as:
QLabel: For displaying text.
QLineEdit: For user input.
QPushButton: For triggering actions.
QComboBox: For selecting options.
QTableWidget: For displaying lists of students, instructors, and courses.
File Structure
main.py: Entry point of the application, initializing the GUI and database connections.
models.py: Contains the definitions of the Person, Student, Instructor, and Course classes.
database.py: Manages database connections and CRUD operations using SQLAlchemy.
ui.py: Defines the layout and functionality of the PyQt5 user interface.
Conclusion
This School Management System project provides a comprehensive solution for managing educational data, enhancing operational efficiency, and ensuring ease of use for administrators, students, and instructors. The class structures and integration with a database form the backbone of the application, enabling smooth functionality and data management.
