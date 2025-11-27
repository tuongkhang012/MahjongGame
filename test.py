class People:
    name: str

    def __init__(self):
        self.age = 2
        self.name = "goon"

    def greeting(self):
        print(f"My name is {self.name}")


class Male(People):
    def __init__(self):
        self.gender = "male"
        super().__init__()

    def greeting(self):
        print(f"My name is {self.name} {self.gender}")

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"

    def __eq__(self, other):
        if not isinstance(other, int):
            return NotImplemented

        return self.name == other.name


class Female(People):
    def __init__(self):
        self.gender = "female"
        super().__init__()

    def greeting(self):
        print(f"My name is {self.name} {self.gender}")


male = Male()
male2 = Male()

if male == male2:
    print("asdasd")
