age = int(input("Enter age: "))
has_id = input("Do you have an ID? (yes/no): ")

if age >= 18:
    if has_id == "yes":
        print("You are allowed to enter.")
    else:
        print("ID required.")
else:
    print("You are underage.")
