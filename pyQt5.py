import sys
import pickle
import csv
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QFileDialog, QFormLayout, QHBoxLayout, QMessageBox, QDialog, QTableView
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from Lab2_Nael import Person, Student, Instructor, Course

class MainWindow(QMainWindow):
    """
    MainWindow class for the School Management System.

    This class provides a graphical user interface (GUI) for managing students,
    instructors, and courses within a school management system. It supports adding,
    editing, deleting, searching, and displaying records, as well as exporting data to CSV files.

    Attributes:
        students (list): List of Student objects.
        instructors (list): List of Instructor objects.
        courses (list): List of Course objects.
    """

    def __init__(self):
        """
        Initializes the MainWindow, sets up the UI, and creates the database.

        :param None: This method does not take any parameters.
        :type None: None
        :raises Exception: May raise an exception during UI setup or database creation.
        :return: None
        :rtype: None
        """
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 800, 600)

        self.students = []
        self.instructors = []
        self.courses = []

        self.initUI()
        self.create_database()
        self.update_table()

    def initUI(self):
        """
        Initializes the user interface components and layout for the School Management System.

        :param None: This method does not take any parameters.
        :type None: None
        :raises Exception: May raise an exception during UI component setup.
        :return: None
        :rtype: None
        """
        layout = QVBoxLayout()

        student_form = QFormLayout()
        self.student_name_entry = QLineEdit()
        self.student_age_entry = QLineEdit()
        self.student_email_entry = QLineEdit()
        self.student_id_entry = QLineEdit()
        student_form.addRow(QLabel("Name"), self.student_name_entry)
        student_form.addRow(QLabel("Age"), self.student_age_entry)
        student_form.addRow(QLabel("Email"), self.student_email_entry)
        student_form.addRow(QLabel("Student ID"), self.student_id_entry)
        add_student_button = QPushButton("Add Student")
        add_student_button.clicked.connect(self.add_student)
        student_form.addRow(add_student_button)
        layout.addWidget(QLabel("Add Student"))
        layout.addLayout(student_form)

        instructor_form = QFormLayout()
        self.instructor_name_entry = QLineEdit()
        self.instructor_age_entry = QLineEdit()
        self.instructor_email_entry = QLineEdit()
        self.instructor_id_entry = QLineEdit()
        instructor_form.addRow(QLabel("Name"), self.instructor_name_entry)
        instructor_form.addRow(QLabel("Age"), self.instructor_age_entry)
        instructor_form.addRow(QLabel("Email"), self.instructor_email_entry)
        instructor_form.addRow(QLabel("Instructor ID"), self.instructor_id_entry)
        add_instructor_button = QPushButton("Add Instructor")
        add_instructor_button.clicked.connect(self.add_instructor)
        instructor_form.addRow(add_instructor_button)
        layout.addWidget(QLabel("Add Instructor"))
        layout.addLayout(instructor_form)

        course_form = QFormLayout()
        self.course_id_entry = QLineEdit()
        self.course_name_entry = QLineEdit()
        self.instructor_dropdown = QComboBox()
        course_form.addRow(QLabel("Course ID"), self.course_id_entry)
        course_form.addRow(QLabel("Course Name"), self.course_name_entry)
        course_form.addRow(QLabel("Assign Instructor"), self.instructor_dropdown)
        add_course_button = QPushButton("Add Course")
        add_course_button.clicked.connect(self.add_course)
        course_form.addRow(add_course_button)
        layout.addWidget(QLabel("Add Course"))
        layout.addLayout(course_form)

        search_layout = QHBoxLayout()
        self.search_entry = QLineEdit()
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_records)
        search_layout.addWidget(QLabel("Search by Name/ID/Course"))
        search_layout.addWidget(self.search_entry)
        search_layout.addWidget(search_button)
        layout.addLayout(search_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Type", "Name/ID", "Additional Info"])
        layout.addWidget(self.table)

        action_buttons = QHBoxLayout()
        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_selected)
        action_buttons.addWidget(delete_button)
        edit_button = QPushButton("Edit Selected")
        edit_button.clicked.connect(self.edit_selected)
        action_buttons.addWidget(edit_button)
        layout.addLayout(action_buttons)

        save_button = QPushButton("Save Data")
        save_button.clicked.connect(self.save_data)
        load_button = QPushButton("Load Data")
        load_button.clicked.connect(self.load_data)
        csv_button = QPushButton("Export to CSV")
        csv_button.clicked.connect(self.export_to_csv)
        view_db_button = QPushButton("View Database")
        view_db_button.clicked.connect(self.view_database)

        layout.addWidget(save_button)
        layout.addWidget(load_button)
        layout.addWidget(csv_button)
        layout.addWidget(view_db_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


    def create_database(self):
        """
        Creates the SQLite database and tables for students, instructors, and courses.

        :param None: This method does not take any parameters.
        :type None: None
        :raises sqlite3.Error: May raise an error if there are issues with database operations.
        :return: None
        :rtype: None
        """
        with sqlite3.connect('school_management.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    age INTEGER,
                    email TEXT,
                    student_id TEXT UNIQUE
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS instructors (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    age INTEGER,
                    email TEXT,
                    instructor_id TEXT UNIQUE
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    course_id TEXT UNIQUE,
                    instructor_id TEXT,
                    FOREIGN KEY (instructor_id) REFERENCES instructors (instructor_id)
                )
            ''')
            conn.commit()


    def update_table(self):
        """
        Updates the table in the UI to reflect the current state of the database,
        loading students, instructors, and courses from the database.

        :param None: This method does not take any parameters.
        :type None: None
        :raises sqlite3.Error: May raise an error if there are issues with database operations.
        :return: None
        :rtype: None
        """
        self.table.setRowCount(0)
        self.students.clear()
        self.instructors.clear()
        self.courses.clear()

        with sqlite3.connect('school_management.db') as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM students")
            for row in cursor.fetchall():
                student = Student(row[1], row[2], row[3], row[4])
                self.students.append(student)
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem("Student"))
                self.table.setItem(row_position, 1, QTableWidgetItem(f"{student.name} ({student.student_id})"))
                self.table.setItem(row_position, 2, QTableWidgetItem(f"Age: {student.age}, Email: {student.getEmail()}"))

            cursor.execute("SELECT * FROM instructors")
            for row in cursor.fetchall():
                instructor = Instructor(row[1], row[2], row[3], row[4])
                self.instructors.append(instructor)
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem("Instructor"))
                self.table.setItem(row_position, 1, QTableWidgetItem(f"{instructor.name} ({instructor.instructor_id})"))
                self.table.setItem(row_position, 2, QTableWidgetItem(f"Age: {instructor.age}, Email: {instructor.getEmail()}"))

            cursor.execute("""
                SELECT courses.*, instructors.name AS instructor_name 
                FROM courses 
                LEFT JOIN instructors ON courses.instructor_id = instructors.instructor_id
            """)
            for row in cursor.fetchall():
                course = Course(row[2], row[1], None)  # Assuming Course constructor takes (course_id, name, instructor)
                self.courses.append(course)
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem("Course"))
                self.table.setItem(row_position, 1, QTableWidgetItem(f" {course.course_id} ,{course.course_name}"))
                self.table.setItem(row_position, 2, QTableWidgetItem(f"Instructor: {row[4] or 'Not assigned'}"))

        self.instructor_dropdown.clear()
        for instructor in self.instructors:
            self.instructor_dropdown.addItem(instructor.name)


    def add_student(self):
        """
        Adds a new student to the database and updates the UI.

        This method retrieves input from the user interface, validates the input,
        and inserts the new student record into the SQLite database. It also updates
        the displayed table in the UI.

        :param None: This method does not take any parameters.
        :type None: None
        :raises ValueError: If the input age is not a valid number.
        :raises sqlite3.Error: May raise an error if there are issues with database operations.
        :return: None
        :rtype: None
        """
        name = self.student_name_entry.text()
        age = self.student_age_entry.text()
        email = self.student_email_entry.text()
        student_id = self.student_id_entry.text()

        if not name or not age or not email or not student_id:
            QMessageBox.warning(self, "Input Error", "All fields must be filled out.")
            return

        try:
            age = int(age)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Age must be a valid number.")
            return

        student = Student(name, age, email, student_id)
        self.students.append(student)

        with sqlite3.connect('school_management.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students (name, age, email, student_id) VALUES (?, ?, ?, ?)", 
                        (student.name, student.age, student.email, student.student_id))
            conn.commit()

        self.update_table()


    def add_instructor(self):
        """
        Adds a new instructor to the database and updates the UI.

        This method retrieves input from the user interface, validates the input,
        and inserts the new instructor record into the SQLite database. It also updates
        the displayed table in the UI.

        :param None: This method does not take any parameters.
        :type None: None
        :raises ValueError: If the input age is not a valid number.
        :raises sqlite3.Error: May raise an error if there are issues with database operations.
        :return: None
        :rtype: None
        """
        name = self.instructor_name_entry.text()
        age = self.instructor_age_entry.text()
        email = self.instructor_email_entry.text()
        instructor_id = self.instructor_id_entry.text()

        if not name or not age or not email or not instructor_id:
            QMessageBox.warning(self, "Input Error", "All fields must be filled out.")
            return

        try:
            age = int(age)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Age must be a valid number.")
            return

        instructor = Instructor(name, age, email, instructor_id)
        self.instructors.append(instructor)

        with sqlite3.connect('school_management.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO instructors (name, age, email, instructor_id) VALUES (?, ?, ?, ?)", 
                        (instructor.name, instructor.age, instructor.email, instructor.instructor_id))
            conn.commit()

        self.update_table()


    def add_course(self):
        """
        Adds a new course to the database and updates the UI.

        This method retrieves input from the user interface for the course ID, 
        course name, and assigned instructor, validates the input, and inserts
        the new course record into the SQLite database. It also updates the
        displayed table in the UI.

        :param None: This method does not take any parameters.
        :type None: None
        :raises sqlite3.Error: May raise an error if there are issues with database operations.
        :return: None
        :rtype: None
        """
        course_id = self.course_id_entry.text()
        name = self.course_name_entry.text()
        instructor_id = self.instructor_dropdown.currentText()  

        if not course_id or not name:
            QMessageBox.warning(self, "Input Error", "Course ID and Name must be filled out.")
            return

        with sqlite3.connect('school_management.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO courses (course_id, name, instructor_id) VALUES (?, ?, ?)", 
                        (course_id, name, instructor_id))
            conn.commit()

        self.update_table()


    def search_records(self):
        """
        Searches for records in the database based on the input and updates the table.

        This method retrieves the search term from the user interface and filters 
        records for students, instructors, and courses based on the provided term. 
        The search is case-insensitive and updates the displayed table to show 
        matching records.

        :param None: This method does not take any parameters.
        :type None: None
        :raises sqlite3.Error: May raise an error if there are issues with database operations.
        :return: None
        :rtype: None
        """
        search_term = self.search_entry.text().lower()
        self.table.setRowCount(0)

        with sqlite3.connect('school_management.db') as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM students WHERE LOWER(name) LIKE ? OR LOWER(student_id) LIKE ?", 
                        (f"%{search_term}%", f"%{search_term}%"))
            for row in cursor.fetchall():
                student = Student(row[1], row[2], row[3], row[4])
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem("Student"))
                self.table.setItem(row_position, 1, QTableWidgetItem(f"{student.name} ({student.student_id})"))
                self.table.setItem(row_position, 2, QTableWidgetItem(f"Age: {student.age}, Email: {student.getEmail()}"))

            cursor.execute("SELECT * FROM instructors WHERE LOWER(name) LIKE ? OR LOWER(instructor_id) LIKE ?", 
                        (f"%{search_term}%", f"%{search_term}%"))
            for row in cursor.fetchall():
                instructor = Instructor(row[1], row[2], row[3], row[4])
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem("Instructor"))
                self.table.setItem(row_position, 1, QTableWidgetItem(f"{instructor.name} ({instructor.instructor_id})"))
                self.table.setItem(row_position, 2, QTableWidgetItem(f"Age: {instructor.age}, Email: {instructor.getEmail()}"))

            cursor.execute(""" 
                SELECT courses.*, instructors.name AS instructor_name 
                FROM courses 
                LEFT JOIN instructors ON courses.instructor_id = instructors.instructor_id
                WHERE LOWER(courses.name) LIKE ? OR LOWER(courses.course_id) LIKE ?
            """, (f"%{search_term}%", f"%{search_term}%"))
            for row in cursor.fetchall():
                course = Course(row[2], row[1], None)
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem("Course"))
                self.table.setItem(row_position, 1, QTableWidgetItem(f"{course.course_id}, {course.course_name}"))
                self.table.setItem(row_position, 2, QTableWidgetItem(f"Instructor: {row[4] or 'Not assigned'}"))


    def delete_selected(self):
        """
        Deletes the selected record from the database and updates the UI.

        This method retrieves the currently selected row in the UI table, 
        determines the type of record (student, instructor, or course), and 
        deletes the corresponding record from the database. If no record is 
        selected, a warning message is displayed.

        :param None: This method does not take any parameters.
        :type None: None
        :raises sqlite3.Error: May raise an error if there are issues with database operations.
        :return: None
        :rtype: None
        """
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Selection Error", "No record selected.")
            return

        record_type = self.table.item(current_row, 0).text()
        if record_type == "Student":
            student_id = self.students[current_row].student_id
            with sqlite3.connect('school_management.db') as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
                conn.commit()
        elif record_type == "Instructor":
            instructor_id = self.instructors[current_row].instructor_id
            with sqlite3.connect('school_management.db') as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM instructors WHERE instructor_id = ?", (instructor_id,))
                conn.commit()
        elif record_type == "Course":
            course_id = self.courses[current_row].course_id
            with sqlite3.connect('school_management.db') as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM courses WHERE course_id = ?", (course_id,))
                conn.commit()

        self.update_table()

    def edit_selected(self):
        """
        Edits the selected record in the database and updates the UI.

        This method retrieves the currently selected row in the UI table, 
        determines the type of record (student, instructor, or course), 
        and allows the user to edit the details of the selected record. 
        If no record is selected, a warning message is displayed.

        :param None: This method does not take any parameters.
        :type None: None
        :raises sqlite3.Error: May raise an error if there are issues with database operations.
        :return: None
        :rtype: None
        """
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Selection Error", "No record selected.")
            return

        record_type = self.table.item(current_row, 0).text()

        if record_type == "Student":
            student = self.students[current_row]
            self.student_name_entry.setText(student.name)
            self.student_age_entry.setText(str(student.age))
            self.student_email_entry.setText(student.email)
            self.student_id_entry.setText(student.student_id)

            if QMessageBox.question(self, "Edit Student", "Do you want to save changes?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                student.name = self.student_name_entry.text()
                student.age = int(self.student_age_entry.text())
                student.email = self.student_email_entry.text()
                student.student_id = self.student_id_entry.text()

                with sqlite3.connect('school_management.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE students 
                        SET name = ?, age = ?, email = ?, student_id = ? 
                        WHERE student_id = ?
                    """, (student.name, student.age, student.email, student.student_id, student.student_id))
                    conn.commit()

        elif record_type == "Instructor":
            instructor = self.instructors[current_row]
            self.instructor_name_entry.setText(instructor.name)
            self.instructor_age_entry.setText(str(instructor.age))
            self.instructor_email_entry.setText(instructor.email)
            self.instructor_id_entry.setText(instructor.instructor_id)

            if QMessageBox.question(self, "Edit Instructor", "Do you want to save changes?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                instructor.name = self.instructor_name_entry.text()
                instructor.age = int(self.instructor_age_entry.text())
                instructor.email = self.instructor_email_entry.text()
                instructor.instructor_id = self.instructor_id_entry.text()

                with sqlite3.connect('school_management.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE instructors 
                        SET name = ?, age = ?, email = ?, instructor_id = ? 
                        WHERE instructor_id = ?
                    """, (instructor.name, instructor.age, instructor.email, instructor.instructor_id, instructor.instructor_id))
                    conn.commit()

        elif record_type == "Course":
            course = self.courses[current_row]
            self.course_id_entry.setText(course.course_id)
            self.course_name_entry.setText(course.course_name)

            self.instructor_dropdown.setCurrentText(course.instructor_id)

            if QMessageBox.question(self, "Edit Course", "Do you want to save changes?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                course.course_id = self.course_id_entry.text()
                course.course_name = self.course_name_entry.text()
                instructor_id = self.instructor_dropdown.currentText() 

                with sqlite3.connect('school_management.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE courses 
                        SET course_id = ?, name = ?, instructor_id = ? 
                        WHERE course_id = ?
                    """, (course.course_id, course.course_name, instructor_id, course.course_id))
                    conn.commit()

        self.update_table()  


    def save_data(self):
        """
        Saves the current data of students and instructors to pickle files.

        This method serializes the lists of students and instructors into
        their respective pickle files. If any errors occur during the 
        file operation, an error message will be displayed.

        :param None: This method does not take any parameters.
        :type None: None
        :raises OSError: May raise an error if there are issues with file operations.
        :return: None
        :rtype: None
        """
        try:
            with open('students.pkl', 'wb') as student_file:
                pickle.dump(self.students, student_file)
            
            with open('instructors.pkl', 'wb') as instructor_file:
                pickle.dump(self.instructors, instructor_file)

            QMessageBox.information(self, "Data Saved", "Data has been saved successfully.")
        except OSError as e:
            QMessageBox.critical(self, "Save Error", f"An error occurred while saving data: {e}")

    def load_data(self):
        """
        Loads students and instructors from pickle files and updates the UI.

        This method deserializes the student and instructor data from 
        their respective pickle files. If any file is not found, a warning
        message will be displayed. The UI is then updated to reflect the 
        loaded data.

        :param None: This method does not take any parameters.
        :type None: None
        :raises FileNotFoundError: Raises an error if the data file is not found.
        :return: None
        :rtype: None
        """
        try:
            with open('students.pkl', 'rb') as student_file:
                self.students = pickle.load(student_file)
        except FileNotFoundError:
            QMessageBox.warning(self, "File Error", "Students data file not found.")
        except Exception as e:
            QMessageBox.critical(self, "Load Error", f"An error occurred while loading students data: {e}")

        try:
            with open('instructors.pkl', 'rb') as instructor_file:
                self.instructors = pickle.load(instructor_file)
        except FileNotFoundError:
            QMessageBox.warning(self, "File Error", "Instructors data file not found.")
        except Exception as e:
            QMessageBox.critical(self, "Load Error", f"An error occurred while loading instructors data: {e}")

        self.update_table()


    def export_to_csv(self):
        """
        Exports the current data of students and instructors to a CSV file.

        This method prompts the user to choose a file location and name for 
        saving the data in CSV format. It includes the details of students, 
        instructors, and courses. If the export is successful, a confirmation 
        message is displayed.

        :param None: This method does not take any parameters.
        :type None: None
        :return: None
        :rtype: None
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if file_name:
            try:
                with open(file_name, 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(["Type", "Name/ID", "Additional Info"])

                    for student in self.students:
                        writer.writerow(["Student", student.name, f"Age: {student.age}, Email: {student.email}, ID: {student.student_id}"])

                    for instructor in self.instructors:
                        writer.writerow(["Instructor", instructor.name, f"Age: {instructor.age}, Email: {instructor.email}, ID: {instructor.instructor_id}"])

                    for course in self.courses:
                        writer.writerow(["Course", course.course_name, f"Course ID: {course.course_id}, Instructor: {course.instructor_id}"])

                QMessageBox.information(self, "Data Exported", "Data has been exported to CSV successfully.")

            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"An error occurred while exporting data: {e}")


    def view_database(self):
        """
        Opens a dialog to view the records in the database in a tabular format.

        This method retrieves data from the students, instructors, and courses 
        tables and displays it in a QTableWidget within a QDialog.
        """
        db_view = QDialog(self)
        db_view.setWindowTitle("Database Records")
        db_view.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()
        table = QTableWidget(db_view)
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Type", "Name/ID", "Additional Info"])
        table.setRowCount(0)

        with sqlite3.connect('school_management.db') as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM students")
            for row in cursor.fetchall():
                student = Student(row[1], row[2], row[3], row[4])
                row_position = table.rowCount()
                table.insertRow(row_position)
                table.setItem(row_position, 0, QTableWidgetItem("Student"))
                table.setItem(row_position, 1, QTableWidgetItem(f"{student.name} ({student.student_id})"))
                table.setItem(row_position, 2, QTableWidgetItem(f"Age: {student.age}, Email: {student.getEmail()}"))

            cursor.execute("SELECT * FROM instructors")
            for row in cursor.fetchall():
                instructor = Instructor(row[1], row[2], row[3], row[4])
                row_position = table.rowCount()
                table.insertRow(row_position)
                table.setItem(row_position, 0, QTableWidgetItem("Instructor"))
                table.setItem(row_position, 1, QTableWidgetItem(f"{instructor.name} ({instructor.instructor_id})"))
                table.setItem(row_position, 2, QTableWidgetItem(f"Age: {instructor.age}, Email: {instructor.getEmail()}"))

            cursor.execute("""
                SELECT courses.*, instructors.name AS instructor_name 
                FROM courses 
                LEFT JOIN instructors ON courses.instructor_id = instructors.instructor_id
            """)
            for row in cursor.fetchall():
                course = Course(row[2], row[1], None)
                row_position = table.rowCount()
                table.insertRow(row_position)
                table.setItem(row_position, 0, QTableWidgetItem("Course"))
                table.setItem(row_position, 1, QTableWidgetItem(f"{course.course_id}, {course.course_name}"))
                table.setItem(row_position, 2, QTableWidgetItem(f"Instructor: {row[4] or 'Not assigned'}"))

        layout.addWidget(table)
        db_view.setLayout(layout)
        db_view.exec_()


    def closeEvent(self, event):
        """
        Handles the close event for the main window.

        This method saves data and performs any necessary cleanup 
        before the application closes. It is called when the user attempts 
        to close the main window.
        
        Args:
            event: The close event that triggers this method.
        """
        self.save_data()
        
        event.accept()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
