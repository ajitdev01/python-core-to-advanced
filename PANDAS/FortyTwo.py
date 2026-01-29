import pandas as pd
df = pd.DataFrame({
    "Name": ["Ajit Kumar", "Nilam Kumar", "Sir", "Mam"]
})

df["Lower"] = df["Name"].str.lower()
df["Length"] = df["Name"].str.len()

print(df)
