import pandas as pd

df = pd.DataFrame({
    "Status": ["pass", "fail", "pass", "fail"]
})

status_map = {"pass": 1, "fail": 0}

df["Result"] = df["Status"].map(status_map)
df["Status"] = df["Status"].replace("fail", "retry")

print(df)
