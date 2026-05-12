class Student:
    def __init__(self, id, name, marks):
        self.id = id
        self.name = name
        self.marks = marks

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, val):
        if val < 0:
            raise ValueError("ID cannot be negative")
        self._id = val
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        self._name = name
    
    @property
    def marks(self):
        return self._marks
    
    @marks.setter
    def marks(self, val):
        if val < 0:
            raise ValueError("Marks cannot be negative")
        self._marks = val

    @staticmethod
    def get_top_student(students):
        top_student = None
        for student in students:
            if top_student is None:
                top_student = student
            elif student.marks > top_student.marks:
                top_student = student
        
        print(f'''
            TOP STUDENT:
            ID: {top_student.id}
            NAME: {top_student.name}
            MARKS: {top_student.marks}
        ''')

s1 = Student(1, "John", 85)

print(s1.id)      # Expected: 1
print(s1.name)    # Expected: John
print(s1.marks)   # Expected: 85

try:
    s2 = Student(-1, "Alice", 90)
except ValueError as e:
    print(e)

try:
    s3 = Student(2, 123, 75)
except ValueError as e:
    print(e)

try:
    s4 = Student(3, "Bob", -50)
except ValueError as e:
    print(e)

students = [
    Student(1, "John", 85),
    Student(2, "Alice", 95),
    Student(3, "Bob", 78)
]

Student.get_top_student(students)