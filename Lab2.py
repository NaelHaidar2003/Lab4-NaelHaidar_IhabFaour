import json
import re

class Person:
    def __init__(self, name, age, email):
        self.name = self.validate_name(name)
        self.age = self.validate_age(age)
        self._email = self.validate_email(email)

    def validate_name(self, name):
        # Regular expression to match names that contain only letters and spaces
        name_regex = r'^[a-zA-Z\s]+$'
        if re.match(name_regex, name):
            return name
        else:
            raise ValueError("Name must contain only letters")
    
    def validate_email(self, email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(email_regex, email):
            return email
        else:
            raise ValueError("Invalid email format")

    def validate_age(self, age):
        if age >= 0:
            return age
        else:
            raise ValueError("Age cannot be negative")

    def get_email(self):
        return self._email

    def set_email(self, new_email):
        self._email = self.validate_email(new_email)

    def introduce(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")

    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'email': self._email
        }

    @staticmethod
    def from_dict(data):
        return Person(data['name'], data['age'], data['email'])


class Course:
    def __init__(self, course_id, course_name, instructor):
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = []

    def add_student(self, student):
        if student not in self.enrolled_students:
            self.enrolled_students.append(student)
            print(f"Student {student.name} has been enrolled")
        else:
            print(f"Student {student.name} is already enrolled")

    def __repr__(self):
        return f"Course({self.course_id}, {self.course_name}, {self.instructor.name})"

    def to_dict(self):
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'instructor_id': self.instructor.instructor_id,
            'enrolled_students': [student.student_id for student in self.enrolled_students]
        }

    @staticmethod
    def from_dict(data, instructors, students):
        instructor = instructors.get(data['instructor_id'])
        course = Course(data['course_id'], data['course_name'], instructor)
        for student_id in data['enrolled_students']:
            student = students.get(student_id)
            course.add_student(student)
        return course


class Student(Person):
    def __init__(self, name, age, email, student_id):
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        if course not in self.registered_courses:
            self.registered_courses.append(course)
            print(f"Course {course.course_name} has been registered.")
        else:
            print(f"Course {course.course_name} is already registered.")

    def to_dict(self):
        person_dict = super().to_dict()
        person_dict.update({
            'student_id': self.student_id,
            'registered_courses': [course.course_id for course in self.registered_courses]
        })
        return person_dict

    @staticmethod
    def from_dict(data, courses):
        student = Student(data['name'], data['age'], data['email'], data['student_id'])
        student.registered_courses = [courses.get(course_id) for course_id in data['registered_courses']]
        return student


class Instructor(Person):
    def __init__(self, name, age, email, instructor_id):
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        if course not in self.assigned_courses:
            self.assigned_courses.append(course)
            print(f"Course {course.course_name} has been assigned")
        else:
            print(f"Course {course.course_name} is already assigned")

    def to_dict(self):
        person_dict = super().to_dict()
        person_dict.update({
            'instructor_id': self.instructor_id,
            'assigned_courses': [course.course_id for course in self.assigned_courses]
        })
        return person_dict

    @staticmethod
    def from_dict(data, courses):
        instructor = Instructor(data['name'], data['age'], data['email'], data['instructor_id'])
        instructor.assigned_courses = [courses.get(course_id) for course_id in data['registered_courses']]

        return instructor


# Serialization functions
def save_to_file(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def load_from_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)


