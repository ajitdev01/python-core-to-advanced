import pandas as pd

df = pd.read_csv("data.csv")

# Apply tax deduction (10%)
df["salary_after_tax"] = df["Salary"].apply(lambda x: x * 0.9)

# Pass if salary >= 50000
df["result"] = df.apply(
    lambda row: "Pass" if row["Salary"] >= 50000 else "Fail",
    axis=1
)

print(df.head())
