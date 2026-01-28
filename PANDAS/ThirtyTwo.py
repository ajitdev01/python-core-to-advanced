import pandas as pd

df = pd.read_csv("data.csv")


df.to_csv("output.csv", index=False)
