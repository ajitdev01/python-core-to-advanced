import pandas as pd 
s = pd.Series([100, 200, 300], index=["x", "y", "z"])

print(s[0])     # By position
print(s["y"])   # By label
