import pandas as pd
scores = [45, 55, 65, 75, 85, 95]

result = pd.qcut(scores, q=3, labels=["Low", "Medium", "High"])
print(result)