class User:
    def __init__(self, name):
        self.name = name

class UserPrinter:
    def print_user(self, user):
        print(f"User: {user.name}")
