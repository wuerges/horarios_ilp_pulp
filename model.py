def id_generator():
    id_seed = 0
    while True:
        yield id_seed
        id_seed += 1



id_seed = id_generator()

class Professor:
    def __init__(self, courses, name):
        self.name = name
        self.courses = courses
        self.id = next(id_seed)

    def __repr__(self):
        return "Prof_%d:%s" % (self.id, self.name)

    def total_time(self):
        return sum(c.num_hours for c in self.courses)

class Course:
    def __init__(self, name, num_hours=4):
        self.name = name
        self.id = next(id_seed)
        self.num_hours = num_hours

    def __repr__(self):
        return "Course_%d:%s" % (self.id, self.name)



# The basic elementary unit of time.
class Slot:
    def __init__(self, name=".", size=1):
        self.name = name
        self.id = next(id_seed)
        self.size = size

    def __repr__(self):
        return "Slot_%d:%s" % (self.id, self.name)

# Consecutive slots where the same course cannot cohexist.
class Shift:
    def __init__(self, slots, name="."):
        self.name = name
        self.id = next(id_seed)
        self.slots = slots

    def __repr__(self):
        return "Shitf_%d:%s" % (self.id, self.name)

# Not very important at this stage.
class Day:
    def __init__(self, slots, name="."):
        self.name = name
        self.id = next(id_seed)
        self.slots = slots

    def __repr__(self):
        return "Day_%d:%s" % (self.id, self.name)

# A Semester to distribute courses
class Semester:
    def __init__(self, slots, name="."):
        self.name = name
        self.courses = []
        self.slots = slots
        self.id = next(id_seed)

    def add_course(self, c):
        self.courses.append(c)

    def __repr__(self):
        return "Semester_%d:%s" % (self.id, self.name)
