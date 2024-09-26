import sqlite3
import json
import re

class Person:
    def __init__(self, name, age, email):
        if not isinstance(name, str) or not name:
            raise ValueError("Name must be a non-empty string")
        if not isinstance(age, int) or age < 0:
            raise ValueError("Age must be a non-negative integer")
        if not self.is_valid_email(email):
            raise ValueError("Invalid email format")
        
        self.name = name
        self.age = age
        self._email = email
        
    def getEmail(self):
        return self._email
    
    def setEmail(self, newEmail):
        if not self.is_valid_email(newEmail):
            raise ValueError("Invalid email format")
        self._email = newEmail
        
    def introduce(self):
        print(f"Personal Information:\n Name: {self.name}. Age: {self.age}")
    
    @staticmethod
    def is_valid_email(email):
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        return re.match(email_regex, email) is not None
    
    def to_dict(self):
        return {"name": self.name, "age": self.age, "_email": self._email}
    
    @staticmethod
    def from_dict(data):
        return Person(data['name'], data['age'], data['_email'])

    # SQLite database interaction methods
    @staticmethod
    def create_table():
        conn = sqlite3.connect('school_management_system.db')
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS Person (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
        ''')
        conn.commit()
        conn.close()

    def save_to_db(self):
        conn = sqlite3.connect('school_management_system.db')
        c = conn.cursor()
        c.execute('''
        INSERT INTO Person (name, age, email) VALUES (?, ?, ?)
        ''', (self.name, self.age, self._email))
        conn.commit()
        conn.close()

    @staticmethod
    def load_from_db(email):
        conn = sqlite3.connect('school_management_system.db')
        c = conn.cursor()
        c.execute('SELECT * FROM Person WHERE email = ?', (email,))
        result = c.fetchone()
        conn.close()
        if result:
            return Person(result[1], result[2], result[3])
        else:
            return None

class Student(Person):
    def __init__(self, name, age, email, student_id):
        super().__init__(name, age, email)
        if not isinstance(student_id, str) or not student_id:
            raise ValueError("Student ID must be a non-empty string")
        
        self.student_id = student_id
        self.registered_courses = []
        
    def register_course(self, course):
        if not isinstance(course, Course):
            raise ValueError("Invalid course")
        self.registered_courses.append(course)
        
    def to_dict(self):
        person_data = super().to_dict()
        person_data.update({"student_id": self.student_id, "registered_courses": self.registered_courses})
        return person_data

    @staticmethod
    def from_dict(data):
        student = Student(data['name'], data['age'], data['_email'], data['student_id'])
        student.registered_courses = data['registered_courses']
        return student

    # SQLite methods
    @staticmethod
    def create_table():
        conn = sqlite3.connect('school_management_system.db')
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS Student (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL UNIQUE,
            student_id TEXT NOT NULL UNIQUE
        )
        ''')
        conn.commit()
        conn.close()

    def save_to_db(self):
        conn = sqlite3.connect('school_management_system.db')
        c = conn.cursor()
        c.execute('''
        INSERT INTO Student (name, age, email, student_id) VALUES (?, ?, ?, ?)
        ''', (self.name, self.age, self._email, self.student_id))
        conn.commit()
        conn.close()

class Instructor(Person):
    def __init__(self, name, age, email, instructor_id):
        super().__init__(name, age, email)
        if not isinstance(instructor_id, str) or not instructor_id:
            raise ValueError("Instructor ID must be a non-empty string")
        
        self.instructor_id = instructor_id
        self.assigned_courses = []
        
    def assign_course(self, course):
        if not isinstance(course, Course):
            raise ValueError("Invalid course")
        self.assigned_courses.append(course)
        
    def to_dict(self):
        person_data = super().to_dict()
        person_data.update({"instructor_id": self.instructor_id, "assigned_courses": self.assigned_courses})
        return person_data

    @staticmethod
    def from_dict(data):
        instructor = Instructor(data['name'], data['age'], data['_email'], data['instructor_id'])
        instructor.assigned_courses = data['assigned_courses']
        return instructor

    # SQLite methods
    @staticmethod
    def create_table():
        conn = sqlite3.connect('school_management_system.db')
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS Instructor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL UNIQUE,
            instructor_id TEXT NOT NULL UNIQUE
        )
        ''')
        conn.commit()
        conn.close()

    def save_to_db(self):
        conn = sqlite3.connect('school_management_system.db')
        c = conn.cursor()
        c.execute('''
        INSERT INTO Instructor (name, age, email, instructor_id) VALUES (?, ?, ?, ?)
        ''', (self.name, self.age, self._email, self.instructor_id))
        conn.commit()
        conn.close()

class Course:
    def __init__(self, course_id, course_name, instructor):
        if not isinstance(course_id, str) or not course_id:
            raise ValueError("Course ID must be a non-empty string")
        if not isinstance(course_name, str) or not course_name:
            raise ValueError("Course name must be a non-empty string")
        
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = []
        
    def add_student(self, student):
        if not isinstance(student, Student):
            raise ValueError("Invalid student")
        self.enrolled_students.append(student)
    
    def to_dict(self):
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "instructor": self.instructor.to_dict(),
            "enrolled_students": [student.to_dict() for student in self.enrolled_students]
        }

    @staticmethod
    def from_dict(data):
        instructor = Instructor.from_dict(data['instructor'])
        course = Course(data['course_id'], data['course_name'], instructor)
        course.enrolled_students = [Student.from_dict(student) for student in data['enrolled_students']]
        return course

    @staticmethod
    
    def create_table():
        conn = sqlite3.connect('school_management_system.db')
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS Course (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id TEXT NOT NULL UNIQUE,
            course_name TEXT NOT NULL,
            instructor_id INTEGER,
            FOREIGN KEY (instructor_id) REFERENCES Instructor(id)
        )
        ''')
        conn.commit()
        conn.close()

    def save_to_db(self):
        conn = sqlite3.connect('school_management_system.db')
        c = conn.cursor()
        c.execute('''
        INSERT INTO Course (course_id, course_name, instructor_id) VALUES (?, ?, (SELECT id FROM Instructor WHERE instructor_id = ?))
        ''', (self.course_id, self.course_name, self.instructor.instructor_id))
        conn.commit()
        conn.close()

Person.create_table()
Student.create_table()
Instructor.create_table()
Course.create_table()
