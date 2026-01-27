import pandas as pd

df = pd.DataFrame({"marks": [70, 80, 90]})
df["grade"] = ["B", "A", "A"]
# print(df)

df = pd.DataFrame({"A": [1, 2, 2, 3]})
print(df.duplicated())
