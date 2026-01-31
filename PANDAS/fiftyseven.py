import pandas as pd

df = pd.DataFrame({
    "Name": ["Ajit", "Nilam", "Rajput"],
    "Subject": ["Math", "Science", "Math"],
    "Marks": [90, 88, 85]
})

result = df.pivot(index="Name", columns="Subject", values="Marks")
print(result)