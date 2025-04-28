import pandas as pd

# Example dataframe
df = pd.DataFrame({
    'A': [1, 2, None, 4],
    'B': [5, None, 7, 8]
})
print(df.head())

# Drop rows where column 'A' is null
df_cleaned = df.dropna(subset=['A'])

print(df_cleaned)
