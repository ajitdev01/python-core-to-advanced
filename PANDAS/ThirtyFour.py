import pandas as pd

df = pd.read_csv("data.csv")


df.to_csv("output.csv", index=False)

df.to_excel("output.xlsx", sheet_name="Result", index=False)
