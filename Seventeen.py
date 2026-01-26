import pandas as pd

data = [
    ["Ajit", 19],
    ["Rahul", 21],
    ["Neha", 20]
]

df = pd.DataFrame(data, columns=["Name", "Age"])
print(df)

print(df.index)
print(df.columns)


print(df["Name"])

print(df[["Name", "Age"]])
