import pandas as pd

df = pd.DataFrame({"marks": [70, 80, 90]})
df["grade"] = ["B", "A", "A"]
# print(df)

df = df.rename(columns={"marks": "Marks"})
print(df)
