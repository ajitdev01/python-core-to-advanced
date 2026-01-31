import pandas as pd

ages = [12, 18, 25, 40, 60]

result =pd.cut(ages, bins=[0, 18, 35, 60], labels=["Teen", "Adult", "Senior"])
print(result)