import pandas as pd

df = pd.read_csv("data.csv")

dept_count = df["Department"].value_counts()
print(dept_count)

