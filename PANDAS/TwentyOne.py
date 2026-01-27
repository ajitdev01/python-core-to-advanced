import pandas as pd

df = pd.DataFrame({"marks": [70, 80, 90]})
df["grade"] = ["B", "A", "A"]
print(df)
