class Bird:
    def sound(self):
        print("Bird sound")

class Sparrow(Bird):
    def sound(self):
        print("Chirp chirp")

b = Sparrow()
b.sound()
