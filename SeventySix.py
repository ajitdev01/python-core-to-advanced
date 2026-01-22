import os

for i, file in enumerate(os.listdir(".")):
    if file.endswith(".txt"):
        os.rename(file, f"file_{i}.txt")
