import pandas as pd

df = pd.read_csv("data.csv")


df_sorted = df.sort_values(by="Age")

df_sorted_multi = df.sort_values(
    by=["Age", "Salary"],
    ascending=[True, False]
)
