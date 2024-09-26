import sys
from PyQt5.QtWidgets import (QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, 
                             QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, 
                             QPushButton, QFormLayout, QTabWidget, QMessageBox, QDialogButtonBox, QDialog, QFileDialog)
from PyQt5.QtCore import Qt
import mysql.connector
from mysql.connector import Error
import csv
import json
from Lab2 import Student, Course, Instructor
from functools import partial

class SchoolManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 800, 600)
        
        # Initialize lists
        self.courses = []  
        self.students = [] 
        self.instructors = []  
        
        # Create the central widget and set layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Create a tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Add tabs
        self.tabs.addTab(self.create_student_form(), "Add Student")
        self.tabs.addTab(self.create_instructor_form(), "Add Instructor")
        self.tabs.addTab(self.create_course_form(), "Add Course")
        self.tabs.addTab(self.register_course_form(), "Register for Course")
        self.tabs.addTab(self.create_table_view(), "View All")
        self.tabs.addTab(self.create_export_import_buttons(), "Save/Load Data")
    
    def update_dropdowns(self):
        # Clear the current items in the dropdowns
        self.student_dropdown.clear()
        self.course_dropdown.clear()
        self.instructor_dropdown.clear()

        # Database connection
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            # Fetch student names
            cursor.execute("SELECT name FROM students")
            student_names = [row[0] for row in cursor.fetchall()]

            # Fetch course names
            cursor.execute("SELECT name FROM courses")
            course_names = [row[0] for row in cursor.fetchall()]

            # Fetch instructor names
            cursor.execute("SELECT name FROM instructors")
            instructor_names = [row[0] for row in cursor.fetchall()]

            # Update dropdown values
            self.student_dropdown.addItems(student_names)
            self.course_dropdown.addItems(course_names)
            self.instructor_dropdown.addItems(instructor_names)

        except mysql.connector.Error as err:
            QMessageBox.information(self, "Database Error", str(err))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


        
    def get_db_connection(self):
        """Establishes a connection to the MySQL database."""
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='school_management_system',
                user='root',
                password='Ihab2003*'
            )
            if connection.is_connected():
                return connection
        except Error as e:
            QMessageBox.critical(None, 'Database Error', str(e))
        return None

    def close_db_connection(self, connection):
        """Closes the connection to the database."""
        if connection is not None and connection.is_connected():
            connection.close()
            QMessageBox.information(None, 'Connection Closed', 'Database connection closed.')
            
    def register_course_form(self):
        layout = QFormLayout()
        
        self.student_dropdown = QComboBox()
        self.course_dropdown = QComboBox()
        
        layout.addRow(QLabel("Select Student:"), self.student_dropdown)
        layout.addRow(QLabel("Select Course:"), self.course_dropdown)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.register_course)
        layout.addWidget(register_button)
        
        register_course_form = QWidget()
        register_course_form.setLayout(layout)
        
        # Update the dropdowns initially
        self.update_dropdowns()
        
        return register_course_form
    
    def create_student_form(self):
        student_form = QWidget()
        layout = QFormLayout()
        
        self.student_name_entry = QLineEdit()
        self.student_age_entry = QLineEdit()
        self.student_email_entry = QLineEdit()
        self.student_id_entry = QLineEdit()
        
        self.add_student_button = QPushButton("Add Student")
        self.add_student_button.clicked.connect(self.add_student)
        
        layout.addRow(QLabel("Name:"), self.student_name_entry)
        layout.addRow(QLabel("Age:"), self.student_age_entry)
        layout.addRow(QLabel("Email:"), self.student_email_entry)
        layout.addRow(QLabel("Student ID:"), self.student_id_entry)
        layout.addRow(self.add_student_button)
        
        student_form.setLayout(layout)
        return student_form

    def create_instructor_form(self):
        instructor_form = QWidget()
        layout = QFormLayout()
        
        self.instructor_name_entry = QLineEdit()
        self.instructor_age_entry = QLineEdit()
        self.instructor_email_entry = QLineEdit()
        self.instructor_id_entry = QLineEdit()
        
        self.add_instructor_button = QPushButton("Add Instructor")
        self.add_instructor_button.clicked.connect(self.add_instructor)
        
        layout.addRow(QLabel("Name:"), self.instructor_name_entry)
        layout.addRow(QLabel("Age:"), self.instructor_age_entry)
        layout.addRow(QLabel("Email:"), self.instructor_email_entry)
        layout.addRow(QLabel("Instructor ID:"), self.instructor_id_entry)
        layout.addRow(self.add_instructor_button)
        
        instructor_form.setLayout(layout)
        return instructor_form

    def create_course_form(self):
        course_form = QWidget()
        layout = QFormLayout()
        
        self.course_id_entry = QLineEdit()
        self.course_name_entry = QLineEdit()
        self.instructor_dropdown = QComboBox()
        
        self.add_course_button = QPushButton("Add Course")
        self.add_course_button.clicked.connect(self.add_course)
        
        layout.addRow(QLabel("Course ID:"), self.course_id_entry)
        layout.addRow(QLabel("Course Name:"), self.course_name_entry)
        layout.addRow(QLabel("Instructor Name:"), self.instructor_dropdown)
        layout.addRow(self.add_course_button)
        
        course_form.setLayout(layout)
        return course_form

    def create_table_view(self):
        table_view = QWidget()
        layout = QVBoxLayout()
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by name, ID, or course...")
        self.search_bar.textChanged.connect(self.update_table_view)
        
        self.table_widget = QTableWidget()
        layout.addWidget(self.search_bar)
        layout.addWidget(self.table_widget)
        
        self.update_table_view()
        
        table_view.setLayout(layout)
        return table_view

    def create_export_import_buttons(self):
        widget = QWidget()
        layout = QVBoxLayout()

        save_button = QPushButton("Save Data")
        save_button.clicked.connect(self.save_data)
        
        load_button = QPushButton("Load Data")
        load_button.clicked.connect(self.load_data)
        
        export_button = QPushButton("Export to CSV")
        export_button.clicked.connect(self.export_to_csv)

        layout.addWidget(save_button)
        layout.addWidget(load_button)
        layout.addWidget(export_button)

        widget.setLayout(layout)
        return widget
    
    def update_table_view(self):
        search_text = self.search_bar.text().lower()
        
        self.table_widget.setRowCount(0)  # Clear previous rows
        self.table_widget.setColumnCount(9)
        self.table_widget.setHorizontalHeaderLabels(["Type", "ID", "Name", "Age", "Email", "Course", "Additional Info", "Edit", "Delete"])
        
        connection = self.get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Fetch Students
        cursor.execute("SELECT * FROM students WHERE LOWER(name) LIKE %s OR LOWER(student_id) LIKE %s", 
                    ('%' + search_text + '%', '%' + search_text + '%'))
        students = cursor.fetchall()

        # Fetch Instructors
        cursor.execute("SELECT * FROM instructors WHERE LOWER(name) LIKE %s OR LOWER(instructor_id) LIKE %s", 
                    ('%' + search_text + '%', '%' + search_text + '%'))
        instructors = cursor.fetchall()

        # Fetch Courses
        cursor.execute("SELECT * FROM courses WHERE LOWER(name) LIKE %s OR LOWER(course_id) LIKE %s", 
                    ('%' + search_text + '%', '%' + search_text + '%'))
        courses = cursor.fetchall()

        row = 0
        
        # Display Students
        for student in students:
            self.table_widget.insertRow(row)
            self.table_widget.setItem(row, 0, QTableWidgetItem("Student"))
            self.table_widget.setItem(row, 1, QTableWidgetItem(student['student_id']))
            self.table_widget.setItem(row, 2, QTableWidgetItem(student['name']))
            self.table_widget.setItem(row, 3, QTableWidgetItem(str(student['age'])))
            self.table_widget.setItem(row, 4, QTableWidgetItem(student['email']))
            self.table_widget.setItem(row, 5, QTableWidgetItem(", ".join(student.get('registered_courses', []))))
            
            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(partial(self.edit_record, row))
            self.table_widget.setCellWidget(row, 7, edit_button)
            
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(partial(self.delete_record, row))
            self.table_widget.setCellWidget(row, 8, delete_button)
            
            row += 1
        
        # Display Instructors
        for instructor in instructors:
            self.table_widget.insertRow(row)
            self.table_widget.setItem(row, 0, QTableWidgetItem("Instructor"))
            self.table_widget.setItem(row, 1, QTableWidgetItem(instructor['instructor_id']))
            self.table_widget.setItem(row, 2, QTableWidgetItem(instructor['name']))
            self.table_widget.setItem(row, 3, QTableWidgetItem(str(instructor['age'])))
            self.table_widget.setItem(row, 4, QTableWidgetItem(instructor['email']))
            self.table_widget.setItem(row, 5, QTableWidgetItem(", ".join(instructor.get('assigned_courses', []))))
            
            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(partial(self.edit_record, row))
            self.table_widget.setCellWidget(row, 7, edit_button)
            
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(partial(self.delete_record, row))
            self.table_widget.setCellWidget(row, 8, delete_button)
            
            row += 1
        
        # Display Courses
        for course in courses:
            self.table_widget.insertRow(row)
            self.table_widget.setItem(row, 0, QTableWidgetItem("Course"))
            self.table_widget.setItem(row, 1, QTableWidgetItem(course['course_id']))
            self.table_widget.setItem(row, 2, QTableWidgetItem(course['name']))
            self.table_widget.setItem(row, 6, QTableWidgetItem(course.get('instructor', '')))
            
            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(partial(self.edit_record, row))
            self.table_widget.setCellWidget(row, 7, edit_button)
            
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(partial(self.delete_record, row))
            self.table_widget.setCellWidget(row, 8, delete_button)
            
            row += 1
        
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        cursor.close()
        connection.close()

    
    def add_student(self):
        name = self.student_name_entry.text()
        age = self.student_age_entry.text()
        email = self.student_email_entry.text()
        student_id = self.student_id_entry.text()
        
        try:
            student = Student(name, int(age), email, student_id)
            connection = self.get_db_connection()
            cursor = connection.cursor()

            cursor.execute("INSERT INTO students (student_id, name, age, email) VALUES (%s, %s, %s, %s)", 
                        (student.student_id, student.name, student.age, student._email))
            connection.commit()

            QMessageBox.information(self, 'Success', f"Student {name} added successfully!")
            
            self.student_name_entry.clear()
            self.student_age_entry.clear()
            self.student_email_entry.clear()
            self.student_id_entry.clear()
            
            self.update_table_view()
            self.update_dropdowns()
        except mysql.connector.Error as err:
            QMessageBox.warning(self, 'Error', str(err))
        except ValueError as e:
            QMessageBox.warning(self, 'Error', str(e))
        finally:
            cursor.close()
            connection.close()

        
        

    def add_instructor(self):
        name = self.instructor_name_entry.text()
        age = self.instructor_age_entry.text()
        email = self.instructor_email_entry.text()
        instructor_id = self.instructor_id_entry.text()
        
        try:
            instructor = Instructor(name, int(age), email, instructor_id)
            connection = self.get_db_connection()
            cursor = connection.cursor()

            cursor.execute("INSERT INTO instructors (instructor_id, name, age, email) VALUES (%s, %s, %s, %s)", 
                        (instructor.instructor_id, instructor.name, instructor.age, instructor._email))
            connection.commit()

            QMessageBox.information(self, 'Success', f"Instructor {name} added successfully!")
            
            self.instructor_name_entry.clear()
            self.instructor_age_entry.clear()
            self.instructor_email_entry.clear()
            self.instructor_id_entry.clear()
            
            self.update_table_view()
            self.update_dropdowns()
        except mysql.connector.Error as err:
            QMessageBox.warning(self, 'Error', str(err))
        except ValueError as e:
            QMessageBox.warning(self, 'Error', str(e))
        finally:
            cursor.close()
            connection.close()

        
    
    def add_course(self):
        course_id = self.course_id_entry.text()
        name = self.course_name_entry.text()
        instructor = self.course_instructor_entry.text()
        
        if not course_id or not name or not instructor:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return
        
        try:
            course = Course(course_id, name, instructor)
            connection=self.get_db_connection()
            cursor = connection.cursor()
            insert_query = """INSERT INTO courses (course_id, name, instructor) 
                              VALUES (%s, %s, %s)"""
            cursor.execute(insert_query, (course.course_id, course.name, course.instructor))
            connection.commit()  

            QMessageBox.information(self, 'Success', f"Course {name} added successfully!")
            self.course_id_entry.clear()
            self.course_name_entry.clear()
            self.course_instructor_entry.clear()
            
            self.update_table_view()
            self.update_dropdowns()
        except Error as e:
            QMessageBox.warning(self, 'Error', str(e))
        finally:
            cursor.close()

    def register_course(self):
        student_name = self.student_dropdown.currentText()
        course_name = self.course_dropdown.currentText()

        try:
            connection=self.get_db_connection()
            cursor = connection.cursor()
            update_query = """UPDATE students 
                              SET course = %s 
                              WHERE name = %s"""
            cursor.execute(update_query, (course_name, student_name))
            connection.commit() 

            self.update_table_view()
        except Error as e:
            QMessageBox.warning(self, 'Error', str(e))
        finally:
            cursor.close()

    def create_edit_dialog(self, item_type, item_data, row):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Edit {item_type}")
        
        layout = QFormLayout()
        
        # Create widgets based on the item type
        if item_type == "Student":
            self.edit_name_entry = QLineEdit(item_data.get('name', ''))
            self.edit_age_entry = QLineEdit(str(item_data.get('age', '')))
            self.edit_email_entry = QLineEdit(item_data.get('email', ''))
            self.edit_id_entry = QLineEdit(item_data.get('student_id', ''))
            
            layout.addRow(QLabel("Name:"), self.edit_name_entry)
            layout.addRow(QLabel("Age:"), self.edit_age_entry)
            layout.addRow(QLabel("Email:"), self.edit_email_entry)
            layout.addRow(QLabel("Student ID:"), self.edit_id_entry)
            
        elif item_type == "Instructor":
            self.edit_name_entry = QLineEdit(item_data.get('name', ''))
            self.edit_age_entry = QLineEdit(str(item_data.get('age', '')))
            self.edit_email_entry = QLineEdit(item_data.get('email', ''))
            self.edit_id_entry = QLineEdit(item_data.get('instructor_id', ''))
            
            layout.addRow(QLabel("Name:"), self.edit_name_entry)
            layout.addRow(QLabel("Age:"), self.edit_age_entry)
            layout.addRow(QLabel("Email:"), self.edit_email_entry)
            layout.addRow(QLabel("Instructor ID:"), self.edit_id_entry)
            
        elif item_type == "Course":
            self.edit_course_id_entry = QLineEdit(item_data.get('course_id', ''))
            self.edit_course_name_entry = QLineEdit(item_data.get('name', ''))
            self.edit_instructor_entry = QLineEdit(item_data.get('instructor', ''))
            
            layout.addRow(QLabel("Course ID:"), self.edit_course_id_entry)
            layout.addRow(QLabel("Course Name:"), self.edit_course_name_entry)
            layout.addRow(QLabel("Instructor Name:"), self.edit_instructor_entry)
        
        # Add Save and Cancel buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.save_changes(item_type, row, dialog))
        buttons.rejected.connect(dialog.reject)
        
        layout.addWidget(buttons)
        dialog.setLayout(layout)
        
        dialog.exec_()

    def edit_record(self, row):
        item_type = self.table_widget.item(row, 0).text()
        
        # Retrieve data based on item type
        if item_type == "Student":
            student_id = self.table_widget.item(row, 1).text()
            item_data = self.fetch_student_data(student_id)
        
        elif item_type == "Instructor":
            instructor_id = self.table_widget.item(row, 1).text()
            item_data = self.fetch_instructor_data(instructor_id)
        
        elif item_type == "Course":
            course_id = self.table_widget.item(row, 2).text()
            item_data = self.fetch_course_data(course_id)
        
        self.create_edit_dialog(item_type, item_data, row)

    def fetch_student_data(self, student_id):
        connection=self.get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        return cursor.fetchone()

    def fetch_instructor_data(self, instructor_id):
        connection=self.get_db_connection()
        cursor = connection.cursor(dictionary=True)        
        cursor.execute("SELECT * FROM instructors WHERE instructor_id = %s", (instructor_id,))
        return cursor.fetchone()

    def fetch_course_data(self, course_id):
        connection=self.get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM courses WHERE course_id = %s", (course_id,))
        return cursor.fetchone()


    def save_changes(self, item_type, row, dialog):
        if item_type == "Student":
            name = self.edit_name_entry.text()
            age = self.edit_age_entry.text()
            email = self.edit_email_entry.text()
            student_id = self.edit_id_entry.text()
            
            conn=self.get_db_connection()
            cursor=conn.cursor()
            cursor.execute("UPDATE students SET name = %s, age = %s, email = %s WHERE student_id = %s", 
                        (name, age, email, student_id))
            conn.commit()
        
        elif item_type == "Instructor":
            name = self.edit_name_entry.text()
            age = self.edit_age_entry.text()
            email = self.edit_email_entry.text()
            instructor_id = self.edit_id_entry.text()
            
            conn=self.get_db_connection()
            cursor=conn.cursor()
            cursor.execute("UPDATE instructors SET name = ?, age = ?, email = ? WHERE instructor_id = ?", 
                        (name, age, email, instructor_id))
            conn.commit()
        
        elif item_type == "Course":
            course_id = self.edit_course_id_entry.text()
            course_name = self.edit_course_name_entry.text()
            instructor = self.edit_instructor_entry.text()
            
            # Update the course record in the database
            conn=self.get_db_connection()
            cursor=conn.cursor()
            cursor.execute("UPDATE courses SET name = ?, instructor = ? WHERE course_id = ?", 
                        (course_name, instructor, course_id))
            conn.commit()
        
        dialog.accept()  # Close the dialog
        self.update_table_view()  # Refresh the table view

    
    def delete_record(self, row):
        item_type = self.table_widget.item(row, 0).text()
        
        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            if item_type == "Student":
                student_id = self.table_widget.item(row, 1).text()
                cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
            
            elif item_type == "Instructor":
                instructor_id = self.table_widget.item(row, 1).text()
                cursor.execute("DELETE FROM instructors WHERE instructor_id = %s", (instructor_id,))
           
            elif item_type == "Course":
                course_id = self.table_widget.item(row, 2).text()
                cursor.execute("DELETE FROM courses WHERE course_id = %s", (course_id,))
           
            conn.commit()
            self.update_table_view()
            self.update_dropdowns()
        except mysql.connector.Error as err:
            QMessageBox.information(self, "Database Error", str(err))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


    
    def save_data(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "JSON Files (*.json);;All Files (*)", options=options)
        
        if file_name:
            data = {
                'students': self.students,
                'instructors': self.instructors,
                'courses': self.courses
            }
            
            try:
                with open(file_name, 'w') as file:
                    json.dump(data, file)
                QMessageBox.information(self, "Save Data", "Data saved successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Save Data", f"Failed to save data: {str(e)}")

    def load_data(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Data", "", "JSON Files (*.json);;All Files (*)")
        
        if not file_name:
            return  # If no file is selected, exit the function

        try:
            with open(file_name, 'r') as file:
                data = json.load(file)  # Load data from the selected JSON file
                
                conn = self.get_db_connection()  # Establish a database connection
                cursor = conn.cursor()  # Create a cursor
                
                # Insert students
                for student in data.get('students', []):
                    cursor.execute(
                        "INSERT INTO students (student_id, name, age, email) VALUES (?, ?, ?, ?)",
                        (student['student_id'], student['name'], student['age'], student['email'])
                    )
                
                # Insert instructors
                for instructor in data.get('instructors', []):
                    cursor.execute(
                        "INSERT INTO instructors (instructor_id, name, age, email) VALUES (?, ?, ?, ?)",
                        (instructor['instructor_id'], instructor['name'], instructor['age'], instructor['email'])
                    )
                
                # Insert courses
                for course in data.get('courses', []):
                    cursor.execute(
                        "INSERT INTO courses (course_id, name, instructor) VALUES (?, ?, ?)",
                        (course['course_id'], course['name'], course['instructor'])
                    )
                
                conn.commit()  # Commit the changes to the database
                
                # Optionally, load data into the local attributes
                self.students = data.get('students', [])
                self.instructors = data.get('instructors', [])
                self.courses = data.get('courses', [])
                
                self.update_table_view()  # Update the UI
                self.update_dropdowns()     # Update dropdowns
                
                QMessageBox.information(self, "Load Data", "Data loaded and inserted successfully.")
        
        except FileNotFoundError:
            QMessageBox.warning(self, "Load Data", "The specified file was not found.")
        except json.JSONDecodeError:
            QMessageBox.warning(self, "Load Data", "Failed to parse JSON data.")
        except Exception as e:
            QMessageBox.warning(self, "Load Data", f"Failed to load data: {str(e)}")
        finally:
            if cursor:
                cursor.close()  # Close the cursor if it was created
            if conn:
                conn.close()

    
    def export_to_csv(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Export CSV", "", "CSV Files (*.csv);;All Files (*)", options=options)
        
        if file_name:
            try:
                with open(file_name, 'w', newline='') as file:
                    writer = csv.writer(file)
                    
        
                    writer.writerow(['Students'])
                    if self.students:
                        headers = self.students[0].keys()
                        writer.writerow(headers)
                        for student in self.students:
                            writer.writerow(student.values())
                    
                    writer.writerow([])
                    writer.writerow(['Instructors'])
                    if self.instructors:
                        headers = self.instructors[0].keys()
                        writer.writerow(headers)
                        for instructor in self.instructors:
                            writer.writerow(instructor.values())
                    
                    writer.writerow([])
                    writer.writerow(['Courses'])
                    if self.courses:
                        headers = self.courses[0].keys()
                        writer.writerow(headers)
                        for course in self.courses:
                            writer.writerow(course.values())
                
                QMessageBox.information(self, "Export CSV", "CSV file exported successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Export CSV", f"Failed to export CSV: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SchoolManagementSystem()
    window.show()
    sys.exit(app.exec_())
