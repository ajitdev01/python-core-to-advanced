import pandas as pd

df = pd.DataFrame({
    "Date": ["01-01-2026", "15-02-2026", "10-03-2026"]
})

df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

print(df)
print(df.dtypes)
