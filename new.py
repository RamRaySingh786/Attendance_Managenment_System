class MyClass:
    def __init__(self,value):
        self._value=value
    def show(self):
        print(f"{self.value}")
    @property

    def value(self):
        return self._value
obj=MyClass(10)
obj.show()       