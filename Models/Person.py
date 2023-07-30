class Person:
    __slots__ = ['id', 'name', 'age']

    def __init__(self, id, name, age):
        self.id = id
        self.name = name
        self.age = age

    def __str__(self):
        return f'Person with name: {self.name} and with age: {self.age} has id: {self.id}'