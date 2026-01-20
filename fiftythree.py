try:
    file = open("sample.txt", "r")
    print(file.read())
except FileNotFoundError:
    print("File not found")
finally:
    print("Program ended")
