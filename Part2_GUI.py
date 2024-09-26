import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import tkinter.filedialog as fd
import json
import os
import mysql.connector
import subprocess
from mysql.connector import Error
import csv
from Lab2 import Student, Instructor, Course  


class SchoolManagementSystem(tk.Tk):
    def __init__(self):
        """
        Initializes the School Management System application.

        This method sets up the main window, initializes data storage for students, instructors,
        and courses, and creates a notebook widget to manage different tabs within the application.
        It also creates and adds frames for each tab and initializes forms for each functionality
        (adding students, adding instructors, adding courses, course registration, and viewing all information).

        Args:
            None

        Returns:
            None
        """
        super().__init__()
        self.title("School Management System")
        self.geometry("1200x600")
        
        # Data Storage
        self.students = []
        self.instructors = []
        self.courses = []

        # Create a notebook to manage tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, expand=1, fill="both")
        
        # Create frames for the notebook tabs
        self.student_frame = ttk.Frame(self.notebook)
        self.instructor_frame = ttk.Frame(self.notebook)
        self.course_frame = ttk.Frame(self.notebook)
        self.register_course_frame = ttk.Frame(self.notebook)
        self.view_all_frame = ttk.Frame(self.notebook)
        
        self.student_frame.pack(fill="both", expand=1)
        self.instructor_frame.pack(fill="both", expand=1)
        self.course_frame.pack(fill="both", expand=1)
        self.register_course_frame.pack(fill="both", expand=1)
        self.view_all_frame.pack(fill="both", expand=1)
        
        # Add frames to the notebook
        self.notebook.add(self.student_frame, text="Add Student")
        self.notebook.add(self.instructor_frame, text="Add Instructor")
        self.notebook.add(self.course_frame, text="Add Course")
        self.notebook.add(self.register_course_frame, text="Course Registration")
        self.notebook.add(self.view_all_frame, text="View All Info")
        
        # Add forms to each frame
        self.create_student_form()
        self.create_instructor_form()
        self.create_course_form()
        self.create_register_course_form()
        self.create_view_all_form()
             
    def get_db_connection(self):
        """
        Establishes a connection to the database.

        This method attempts to connect to the MySQL database using the provided
        connection details. If the connection is successful, it returns the connection object.

        Args:
            None

        Returns:
            connection (mysql.connector.connection_cext.CMySQLConnection): The database connection object, or None if the connection fails.
        """ 
        
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
            messagebox.showerror('Database Error', str(e))
        return None

    def close_db_connection(self, connection):
        """
        Closes the database connection.

        This method checks if the provided connection is active and closes it.

        Args:
            connection (mysql.connector.connection_cext.CMySQLConnection): The database connection object.

        Returns:
            None
        """
        if connection.is_connected():
            connection.close()
            
    def create_student_form(self):
        """
        Creates the form for adding a student.

        This method initializes the form fields (Name, Age, Email, Student ID) and
        adds a button to submit the student information to the database.

        Args:
            None

        Returns:
            None
        """
        tk.Label(self.student_frame, text="Name:").pack()
        self.student_name_entry = tk.Entry(self.student_frame)
        self.student_name_entry.pack()
        
        tk.Label(self.student_frame, text="Age:").pack()
        self.student_age_entry = tk.Entry(self.student_frame)
        self.student_age_entry.pack()
        
        tk.Label(self.student_frame, text="Email:").pack()
        self.student_email_entry = tk.Entry(self.student_frame)
        self.student_email_entry.pack()
        
        tk.Label(self.student_frame, text="Student ID:").pack()
        self.student_id_entry = tk.Entry(self.student_frame)
        self.student_id_entry.pack()
        
        self.add_student_button = tk.Button(self.student_frame, text="Add Student", command=self.add_student)
        self.add_student_button.pack()
    
    def create_instructor_form(self):
        """
        Creates the form for adding an instructor.

        This method initializes the form fields (Name, Age, Email, Instructor ID) and
        adds a button to submit the instructor information to the database.

        Args:
            None

        Returns:
            None
        """
        tk.Label(self.instructor_frame, text="Name:").pack()
        self.instructor_name_entry = tk.Entry(self.instructor_frame)
        self.instructor_name_entry.pack()
        
        tk.Label(self.instructor_frame, text="Age:").pack()
        self.instructor_age_entry = tk.Entry(self.instructor_frame)
        self.instructor_age_entry.pack()
        
        tk.Label(self.instructor_frame, text="Email:").pack()
        self.instructor_email_entry = tk.Entry(self.instructor_frame)
        self.instructor_email_entry.pack()
        
        tk.Label(self.instructor_frame, text="Instructor ID:").pack()
        self.instructor_id_entry = tk.Entry(self.instructor_frame)
        self.instructor_id_entry.pack()
        
        self.add_instructor_button = tk.Button(self.instructor_frame, text="Add Instructor", command=self.add_instructor)
        self.add_instructor_button.pack()
    
    def create_course_form(self):
        """
        Creates the form for adding a course.

        This method initializes the form fields (Course ID, Course Name, Instructor Name) and
        adds a button to submit the course information to the database.

        Args:
            None

        Returns:
            None
        """
        tk.Label(self.course_frame, text="Course ID:").pack()
        self.course_id_entry = tk.Entry(self.course_frame)
        self.course_id_entry.pack()
        
        tk.Label(self.course_frame, text="Course Name:").pack()
        self.course_name_entry = tk.Entry(self.course_frame)
        self.course_name_entry.pack()
        
        tk.Label(self.course_frame, text="Instructor Name:").pack()
        self.instructor_dropdown = ttk.Combobox(self.course_frame)
        self.instructor_dropdown.pack()
        
        self.add_course_button = tk.Button(self.course_frame, text="Add Course", command=self.add_course)
        self.add_course_button.pack()
        
    def create_register_course_form(self):
        """
        Creates the form for registering a student for a course.

        This method initializes the form fields (Select Student, Select Course) and
        adds a button to submit the registration information to the database.

        Args:
            None

        Returns:
            None
        """
        tk.Label(self.register_course_frame, text="Select Student").pack()
        self.student_dropdown = ttk.Combobox(self.register_course_frame)
        self.student_dropdown.pack()
        
        tk.Label(self.register_course_frame, text="Select Course").pack()
        self.course_dropdown = ttk.Combobox(self.register_course_frame)
        self.course_dropdown.pack()
        
        tk.Button(self.register_course_frame, text="Register", command=self.register_course).pack()
        self.refresh_dropdowns()
    
    def create_view_all_form(self):
        """
        Creates the form for viewing all information.

        This method initializes the search bar and the table for displaying all information
        (ID, Name, Age, Email, Additional Info, Actions). It also adds buttons for refreshing
        the table, exporting data to CSV, saving data, and loading data.

        Args:
            None

        Returns:
            None
        """
        search_frame = tk.Frame(self.view_all_frame)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_records).pack(side=tk.LEFT)
        
        self.view_all_table = ttk.Treeview(self.view_all_frame, columns=("ID", "Name", "Age", "Email", "Additional Info", "Actions"), show="headings")
        self.view_all_table.heading("ID", text="ID") 
        self.view_all_table.heading("Name", text="Name")
        self.view_all_table.heading("Age", text="Age")
        self.view_all_table.heading("Email", text="Email")
        self.view_all_table.heading("Additional Info", text="Additional Info")
        self.view_all_table.heading("Actions", text="Actions")
        self.view_all_table.pack(expand=1, fill="both")
        
        button_frame = tk.Frame(self.view_all_frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Refresh", command=self.refresh_view_all).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Export to CSV", command=self.export_to_csv).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Save Data", command=self.save_data).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Load Data", command=self.load_data).pack(side=tk.LEFT, padx=5)
    
    def refresh_view_all(self):
        """
        Refreshes and displays all students, instructors, and courses in the table.

        Parameters:
        self: Instance of the class.

        Returns:
        None

        Functionality:
        - Clears the existing table data.
        - Establishes a database connection and fetches all students, instructors, and courses.
        - Inserts the fetched data into the table for display.
        - Binds the click event on the table to handle editing or deleting records.

        Example:
        self.refresh_view_all()
        """
        # Clear existing table data
        self.view_all_table.delete(*self.view_all_table.get_children())
        
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            # Fetch students
            cursor.execute("SELECT student_id, name, age, email FROM students")
            self.students = cursor.fetchall()  

            # Fetch instructors
            cursor.execute("SELECT instructor_id, name, age, email FROM instructors")
            self.instructors = cursor.fetchall() 

            # Fetch courses
            cursor.execute("SELECT course_id, name, instructor_name FROM courses")
            self.courses = cursor.fetchall()  

            # Display Students
            for student in self.students:
                self.view_all_table.insert("", tk.END, values=(
                    student[0],  # student_id
                    student[1],  # name
                    student[2],  # age
                    student[3],  # email
                    "Student",
                    "Edit/Delete"
                ))
            
            # Display Instructors
            for instructor in self.instructors:
                self.view_all_table.insert("", tk.END, values=(
                    instructor[0],  
                    instructor[1],  
                    instructor[2],  
                    instructor[3],  
                    "Instructor",
                    "Edit/Delete"
                ))
            
            # Display Courses
            for course in self.courses:
                self.view_all_table.insert("", tk.END, values=(
                    course[0],  
                    course[1],  
                    "-",  
                    "-",  
                    f"Instructor: {course[2]}",  # instructor
                    "Edit/Delete"
                ))

            # Bind the click event
            self.view_all_table.bind("<ButtonRelease-1>", self.handle_table_click)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


    def handle_table_click(self, event):
        """
        Handles click events on the table, allowing for editing or deleting records.

        Parameters:
        self: Instance of the class.
        event: The event object that triggered the method.

        Returns:
        None

        Functionality:
        - Identifies the clicked row and retrieves the record ID and type.
        - Prompts the user to choose between editing or deleting the record.
        - Calls the appropriate method based on the user's choice.

        Example:
        self.view_all_table.bind("<ButtonRelease-1>", self.handle_table_click)
        """
        item = self.view_all_table.identify_row(event.y)
        if not item:
            return
        record_id = self.view_all_table.item(item, "values")[0]
        record_type = self.view_all_table.item(item, "values")[4]
        action = self.view_all_table.item(item, "values")[5]
        
        if action == "Edit/Delete":
            action = messagebox.askyesno("Action", "Do you want to edit this record?")
            if action:
                self.edit_record(record_type, record_id)
            else:
                confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
                if confirm:
                    self.delete_record(record_type, record_id)


    def register_course(self):
        """
        Registers a student for a selected course.

        Parameters:
        self: Instance of the class.

        Returns:
        None

        Functionality:
        - Retrieves selected student and course names from the dropdown menus.
        - Validates that both a student and course are selected.
        - Inserts the registration data into the database and commits the transaction.
        - Displays a success message upon successful registration.

        Example:
        self.register_course()
        """
        student_name = self.student_dropdown.get()
        course_name = self.course_dropdown.get()

        
        if not student_name or not course_name:
            messagebox.showwarning("Registration Error", "Please select both student and course.")
            return
        
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO course_registrations (student_name, course_name) VALUES (%s, %s)",
                (student_name, course_name)
            )
            conn.commit()
            print(f"Course {course_name} is registered by {student_name}")
            messagebox.showinfo("Registration Successful", f"Course {course_name} has been registered by {student_name}.")
        except Error as e:
            messagebox.showwarning("Database Error", str(e))
        
    def refresh_dropdowns(self):
        """
        Refreshes the values in the student, course, and instructor dropdown menus.

        Parameters:
        self: Instance of the class.

        Returns:
        None

        Functionality:
        - Clears existing values in the dropdown menus.
        - Establishes a database connection and fetches all student names, course names, and instructor names.
        - Updates the dropdown menus with the fetched values.

        Example:
        self.refresh_dropdowns()
        """
        self.student_dropdown["values"] = []
        self.course_dropdown["values"] = []
        self.instructor_dropdown["values"]= []

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
            
            cursor.execute("SELECT name FROM instructors")
            instructor_name= [row[0] for row in cursor.fetchall()]

            # Update dropdown values
            self.student_dropdown["values"] = student_names
            self.course_dropdown["values"] = course_names
            self.instructor_dropdown["values"] = instructor_name

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    
    def add_student(self):
        """
        Adds a new student to the database and updates the UI.

        Parameters:
        self: Instance of the class.

        Returns:
        None

        Functionality:
        - Retrieves the student's name, age, email, and ID from the input fields.
        - Validates that all fields are filled.
        - Creates a new Student object and inserts it into the database.
        - Updates the student list and refreshes the dropdown menus and the display table.
        - Clears the input fields after adding the student.
        - Handles and displays any input or database errors.

        Example:
        self.add_student()
        """
        name = self.student_name_entry.get()
        age = self.student_age_entry.get()
        email = self.student_email_entry.get()
        student_id = self.student_id_entry.get()
        
        if not name or not age or not email or not student_id:
            messagebox.showwarning("Input Error", "Enter all required fields")
            return
        
        try:
            student = Student(name, int(age), email, student_id)

            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO students (student_id, name, age, email) VALUES (%s, %s, %s, %s)",
                (student.student_id, student.name, student.age, student._email)
            )
            conn.commit()
            self.students.append(student)
            messagebox.showinfo("Add Student", f"Added Student: {student.name}, {student.age}, {student._email}, {student.student_id}")
            self.refresh_dropdowns()
            self.refresh_view_all()
            
            self.student_name_entry.delete(0, tk.END)
            self.student_age_entry.delete(0, tk.END)
            self.student_email_entry.delete(0, tk.END)
            self.student_id_entry.delete(0, tk.END)
            self.close_db_connection(conn)

        except ValueError as ve:
            messagebox.showwarning("Input Error", str(ve))
        except Error as e:
            messagebox.showwarning('Database Error', str(e))
            
    def add_instructor(self):
        """
        Adds a new instructor to the database and updates the UI.

        Parameters:
        self: Instance of the class.

        Returns:
        None

        Functionality:
        - Retrieves the instructor's name, age, email, and ID from the input fields.
        - Validates that all fields are filled.
        - Creates a new Instructor object and inserts it into the database.
        - Updates the instructor list and refreshes the dropdown menus and the display table.
        - Clears the input fields after adding the instructor.
        - Handles and displays any input or database errors.

        Example:
        self.add_instructor()
        """
        name = self.instructor_name_entry.get()
        age = self.instructor_age_entry.get()
        email = self.instructor_email_entry.get()
        instructor_id = self.instructor_id_entry.get()
        
        if not name or not age or not email or not instructor_id:
            messagebox.showwarning("Input Error", "Enter all required fields")
            return
        
        try:
            instructor = Instructor(name, int(age), email, instructor_id)

            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO instructors (instructor_id, name, age, email) VALUES (%s, %s, %s, %s)",
                (instructor.instructor_id, instructor.name, instructor.age, instructor._email)
            )
            conn.commit()
            self.instructors.append(instructor)
            messagebox.showinfo("Add Instructor", f"Added Instructor: {instructor.name}, {instructor.age}, {instructor._email}, {instructor.instructor_id}")
            self.refresh_dropdowns()
            self.refresh_view_all()
            
            self.instructor_name_entry.delete(0, tk.END)
            self.instructor_age_entry.delete(0, tk.END)
            self.instructor_email_entry.delete(0, tk.END)
            self.instructor_id_entry.delete(0, tk.END)
            
            self.close_db_connection(conn)
        except ValueError as ve:
            messagebox.showwarning("Input Error", str(ve))
        except Error as e:
            messagebox.showwarning('Database Error', str(e))
            
    
    def add_course(self):
        """
        Adds a new course to the database and updates the UI.

        Parameters:
        self: Instance of the class.

        Returns:
        None

        Functionality:
        - Retrieves the course's ID, name, and instructor name from the input fields.
        - Validates that all fields are filled.
        - Creates a new Course object and inserts it into the database.
        - Updates the course list and refreshes the dropdown menus and the display table.
        - Clears the input fields after adding the course.
        - Handles and displays any input or database errors.

        Example:
        self.add_course()
        """
        course_id = self.course_id_entry.get()
        course_name = self.course_name_entry.get()
        instructor_name = self.instructor_dropdown.get()
        
        if not course_id or not course_name or not instructor_name:
            messagebox.showwarning("Input Error", "Enter all required fields")
            return
        
        try:
            course = Course(course_id, course_name, instructor_name)

            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO courses (course_id, name, instructor_name) VALUES (%s, %s, %s)",
                (course.course_id, course.course_name, course.instructor)
            )
            conn.commit()
            self.courses.append(course)
            messagebox.showinfo("Add Course", f"Added Course: {course_id}, {course_name}, {instructor_name}")
            self.refresh_dropdowns()
            self.refresh_view_all()
            
            self.course_id_entry.delete(0, tk.END)
            self.course_name_entry.delete(0, tk.END)
            self.instructor_dropdown.delete(0, tk.END)
            
            self.close_db_connection(conn)
        except ValueError as ve:
            messagebox.showwarning("Input Error", str(ve))
        except Error as e:
            messagebox.showwarning('Database Error', str(e))
            
    
    def search_records(self):
        """
        Searches for students, instructors, and courses in the database.

        Parameters:
        self: Instance of the class.

        Returns:
        None

        Functionality:
        - Retrieves the search term from the search entry field.
        - Clears the current entries in the display table.
        - Filters the student, instructor, and course lists based on the search term.
        - Updates the display table with the filtered results.

        Example:
        self.search_records()
        """
        search_term = self.search_entry.get().lower()
        for row in self.view_all_table.get_children():
            self.view_all_table.delete(row)
        
        # Filter and display students
        for student in self.students:
            student_id, student_name, student_age, student_email = student
            if search_term in student_name.lower() or search_term in str(student_id).lower() or search_term in "student":
                self.view_all_table.insert("", tk.END, values=(
                    student_id,
                    student_name,
                    student_age,
                    student_email,
                    "Student",
                    "Edit/Delete"
                ))
        
        # Filter and display instructors
        for instructor in self.instructors:
            instructor_id, instructor_name, instructor_age, instructor_email = instructor
            if search_term in instructor_name.lower() or search_term in str(instructor_id).lower() or search_term in "instructor":
                self.view_all_table.insert("", tk.END, values=(
                    instructor_id,
                    instructor_name,
                    instructor_age,
                    instructor_email,
                    "Instructor",
                    "Edit/Delete"
                ))
        
        # Filter and display courses
        for course in self.courses:
            course_id, course_name, course_instructor = course
            if search_term in course_name.lower() or search_term in str(course_id).lower() or search_term in "course":
                self.view_all_table.insert("", tk.END, values=(
                    course_id,
                    course_name,
                    "-",  # No age for courses
                    "-",  # No email for courses
                    f"Instructor: {course_instructor}",
                    "Edit/Delete"
                ))


    
    def save_data(self):
        """
        Opens a file dialog to save student, instructor, and course data in JSON format.

        If a valid file path is selected, the current data of students, instructors,
        and courses is serialized to JSON and written to the specified file. A message
        box is displayed to inform the user of the success of the operation.
        """
        file_path = fd.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Data"
        )
        
        if file_path:
            data = {
                "students": self.students,
                "instructors": self.instructors,
                "courses": self.courses
            }
            with open(file_path, "w") as f:
                json.dump(data, f)
            messagebox.showinfo("Save Data", f"Data saved successfully to {file_path}!")

    def load_data(self):
        """
        Opens a file dialog to load student, instructor, and course data from a JSON file.

        If a valid file path is selected, the data is read from the JSON file and
        deserialized into the respective attributes. The method inserts the data into
        the database, updating existing records if they exist. A message box informs the
        user about the success or failure of the loading process.
        """
        file_path = fd.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Open Data"
        )
        
        if file_path:
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    data = json.load(f)
                    self.students = data.get("students", [])
                    self.instructors = data.get("instructors", [])
                    self.courses = data.get("courses", [])
                    
                    try:
                        conn = self.get_db_connection()
                        cursor = conn.cursor()
                        
                        # Insert students into the database
                        for student in self.students:
                            cursor.execute(
                                "INSERT INTO students (student_id, name, age, email) VALUES (%s, %s, %s, %s) "
                                "ON DUPLICATE KEY UPDATE name = VALUES(name), age = VALUES(age), email = VALUES(email)",
                                (student[0], student[1], student[2], student[3])
                            )
                        
                        # Insert instructors into the database
                        for instructor in self.instructors:
                            cursor.execute(
                                "INSERT INTO instructors (instructor_id, name, age, email) VALUES (%s, %s, %s, %s) "
                                "ON DUPLICATE KEY UPDATE name = VALUES(name), age = VALUES(age), email = VALUES(email)",
                                (instructor[0], instructor[1], instructor[2], instructor[3])
                            )
                        
                        # Insert courses into the database
                        for course in self.courses:
                            cursor.execute(
                                "INSERT INTO courses (course_id, name, instructor_name) VALUES (%s, %s, %s) "
                                "ON DUPLICATE KEY UPDATE name = VALUES(name), instructor_name = VALUES(instructor_name)",
                                (course[0], course[1], course[2])
                            )
                        
                        conn.commit()
                        self.refresh_view_all()
                        self.refresh_dropdowns()
                        messagebox.showinfo("Load Data", f"Data loaded successfully from {file_path} and inserted into the database!")
                        
                        self.close_db_connection(conn)
                    except Error as e:
                        messagebox.showwarning("Database Error", str(e))
            else:
                messagebox.showwarning("Load Data", "The selected file does not exist!")
    
    def edit_record(self, record_type, record_id):
        """
        Opens an edit dialog for the specified record type and record ID.

        It fetches the record from the database and populates the dialog with its data,
        allowing the user to make changes. If the record is found, the dialog is opened;
        otherwise, a warning message is displayed. 

        Args:
            record_type (str): The type of record to edit (e.g., "Student", "Instructor").
            record_id (int): The unique identifier of the record to be edited.
        """
        conn = self.get_db_connection()
        if not conn:
            return

        try:
            cursor = conn.cursor(dictionary=True)

            record = None
            if record_type == "Student":
                cursor.execute("SELECT * FROM students WHERE student_id = %s", (record_id,))
                record = cursor.fetchone()
            elif record_type == "Instructor":
                cursor.execute("SELECT * FROM instructors WHERE instructor_id = %s", (record_id,))
                record = cursor.fetchone()
            elif record_type.startswith("Instructor:"):
                cursor.execute("SELECT * FROM courses WHERE course_id = %s", (record_id,))
                record = cursor.fetchone()

            if record:
                self.open_edit_dialog(record_type, record, conn)
            else:
                messagebox.showwarning("Edit Error", "Record not found!")
                self.close_db_connection(conn)
        except Error as e:
            messagebox.showerror("Database Error", str(e))
            self.close_db_connection(conn)

    def open_edit_dialog(self, record_type, record, conn):
        """
        Creates a dialog for editing a record with the specified type and data.

        The dialog allows the user to update the name, age, and email fields (if applicable)
        and save the changes back to the database.

        Args:
            record_type (str): The type of record being edited.
            record (dict): The record data to populate the dialog with.
            conn (Connection): The database connection to perform updates.
        """
        def save_changes():
            new_name = name_entry.get()
            if not record_type.startswith("Instructor:"):
                new_age = age_entry.get()
                new_email = email_entry.get()

            try:
                cursor = conn.cursor()
                if record_type == "Student":
                    cursor.execute("UPDATE students SET name = %s, age = %s, email = %s WHERE student_id = %s",
                                (new_name, new_age, new_email, record['student_id']))
                elif record_type == "Instructor":
                    cursor.execute("UPDATE instructors SET name = %s, age = %s, email = %s WHERE instructor_id = %s",
                                (new_name, new_age, new_email, record['instructor_id']))
                elif record_type.startswith("Instructor:"):
                    cursor.execute("UPDATE courses SET name = %s WHERE course_id = %s",
                                (new_name, record['course_id']))

                conn.commit()
                self.refresh_view_all()
                edit_window.destroy()
                self.close_db_connection(conn)
            except Error as e:
                messagebox.showerror("Database Error", str(e))
                conn.rollback()
                self.close_db_connection(conn)

        edit_window = tk.Toplevel(self)
        edit_window.title(f"Edit {record_type}")

        tk.Label(edit_window, text="Name:").pack()
        name_entry = tk.Entry(edit_window)
        name_entry.insert(0, record['name'])
        name_entry.pack()

        if not record_type.startswith("Instructor:"):
            tk.Label(edit_window, text="Age:").pack()
            age_entry = tk.Entry(edit_window)
            age_entry.insert(0, record.get('age', ''))
            age_entry.pack()

            tk.Label(edit_window, text="Email:").pack()
            email_entry = tk.Entry(edit_window)
            email_entry.insert(0, record['email'])
            email_entry.pack()

        save_button = tk.Button(edit_window, text="Save Changes", command=save_changes)
        save_button.pack()
        
        self.refresh_dropdowns()
        self.refresh_view_all()



    def backup_database(self):
        """
        Opens a file dialog to specify the location to save a backup of the database.

        The backup is created using the `mysqldump` command. A message box is displayed to
        inform the user of the success or failure of the operation.
        """
        file_path = fd.asksaveasfilename(
            defaultextension=".sql",
            filetypes=[("SQL files", "*.sql"), ("All files", "*.*")],
            title="Save Database Backup"
        )
        
        if file_path:
            try:
                subprocess.run(
                    ["mysqldump", "-u", "root", "-p", "school_management_system", ">", file_path],
                    shell=True,
                    check=True
                )
                messagebox.showinfo("Backup Database", f"Database backup saved to {file_path} successfully!")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Backup Error", str(e))
                
    def delete_record(self, record_type, record_id):
        """
        Deletes a record of the specified type and ID from the database.

        The method attempts to delete the record and commits the changes. If an error occurs,
        the transaction is rolled back and an error message is displayed.

        Args:
            record_type (str): The type of record to delete (e.g., "Student", "Instructor").
            record_id (int): The unique identifier of the record to be deleted.
        """
        conn = self.get_db_connection()
        
        if not conn:
            return

        try:
            cursor = conn.cursor()

            if record_type == "Student":
                cursor.execute("DELETE FROM students WHERE student_id = %s", (record_id,))
            elif record_type == "Instructor":
                cursor.execute("DELETE FROM instructors WHERE instructor_id = %s", (record_id,))
            elif record_type.startswith("Instructor:"):
                cursor.execute("DELETE FROM courses WHERE course_id = %s", (record_id,))

            conn.commit()
        except mysql.connector.Error as e:
            conn.rollback()
            messagebox.showerror("Delete Error", f"An error occurred: {e}")
        finally:
            # Close the connection
            self.close_db_connection(conn)
        
        self.refresh_view_all()
        self.refresh_dropdowns()
        
    def export_to_csv(self):
        """
        Opens a file dialog to specify the location to save exported data in CSV format.

        The method fetches data from the database for students, instructors, and courses,
        writing it to the specified CSV file. A message box is displayed to inform the user
        of the success or failure of the operation.
        """
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Name", "Age", "Email", "Additional Info", "Type"])
                
                # Fetch students from database
                cursor.execute("SELECT * FROM students")
                students = cursor.fetchall()
                for student in students:
                    writer.writerow([student[0], student[1], student[2], student[3], "Student", ""])
                
                # Fetch instructors from database
                cursor.execute("SELECT * FROM instructors")
                instructors = cursor.fetchall()
                for instructor in instructors:
                    writer.writerow([instructor[0], instructor[1], instructor[2], instructor[3], "Instructor", ""])
                
                # Fetch courses from database
                cursor.execute("SELECT * FROM courses")
                courses = cursor.fetchall()
                for course in courses:
                    writer.writerow([course[0], course[1], "-", "-", f"Instructor: {course[2]}", "Course"])
            
            messagebox.showinfo("Export to CSV", "Data exported successfully!")
        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred while exporting data to CSV: {str(e)}")
        finally:
            if conn:
                self.close_db_connection(conn)


# Run the application
if __name__ == "__main__":
    app = SchoolManagementSystem()
    app.mainloop()