import pandas as pd

df = pd.read_csv("data.csv")


# df.to_csv("output.csv", index=False)

df = pd.read_excel("data.xlsx", sheet_name="Sheet1")
print(df.head())

