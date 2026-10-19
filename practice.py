class Students:
    def __init__(self):
        self.total_students = 500

    def add_student(self):
        self.total_students+=1

class University:
    def __init__(self):
        self.name = "Stanford University"
        self.students = Students()

university = University()

print(university.name)


university.students.add_student()
university.students.add_student()

print(university.students.total_students)