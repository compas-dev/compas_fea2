class Parent1():
    """
    Foo Class.
    This class foos around.
    """
    def __init__(self):
        self.id = 'Base'

class Child1(Parent1):
    def __init__(self):
        super().__init__()
        self.id ='A'

class Parent2(Parent1):
    def __init__(self):
        super().__init__()
        self.id ='B'

class Child2(Parent2):
    def __init__(self):
        super().__init__()
        self.id ='C'

if __name__ == "__main__":
    p1 = Parent1()
    c1 = Child1()
    p2 = Parent2()
    c2 = Child2()

    print(p1.__doc__, c1.__doc__, p2.id, c2.id)
