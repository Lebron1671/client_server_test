from Models.Person import Person


class AVLNode:
    def __init__(self, person: Person):
        self.person = person
        self.left = None
        self.right = None
        self.height = 1