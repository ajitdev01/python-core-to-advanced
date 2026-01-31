import pandas as pd
df = pd.DataFrame({
    "Name": ["Ajit", "Nilam ❤️"],
    "Math": [90, 85],
    "Science": [88, 92]
})

result = pd.melt(df, id_vars="Name", var_name="Subject", value_name="Marks")
print(result)
