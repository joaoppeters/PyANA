import numpy as np
import os
import pandas as pd


pwd = os.path.dirname(os.path.dirname(__file__))

data = pd.read_csv(
    pwd + "\\sistemas\\demanda_maxima.csv",
    encoding="utf-8",
    header=None,
    skiprows=2,
    skipfooter=2,
    usecols=np.r_[4:316],
)

months = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
]

# Create the new 10x12 DataFrame with proper indexing
df_rearranged = pd.DataFrame(
    0, index=[f"Ano {y}" for y in range(1999, 2025)], columns=months
)

# Extract the diagonal values and reshape them into (10,12)
diagonal_values = [data.iloc[i, i] for i in range(data.shape[1])]  # Get diagonal values
reshaped_values = np.array(diagonal_values).reshape(26, 12)  # Reshape into (10x12)

# Assign values to the new DataFrame
df_rearranged.iloc[:, :] = reshaped_values
df_rearranged = df_rearranged.T

# Display the rearranged DataFrame
print(
    df_rearranged.describe().loc[
        [
            "std",
        ]
    ]
)

print()

# import pandas as pd
# import numpy as np

# # Define months and years
# months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
# years = range(1, 11)

# # Create column labels by repeating months 10 times (one set for each year)
# columns = [f"{month} Year {year}" for year in years for month in months]

# # Create index with each year repeating 12 times (for each month)
# index = np.repeat(range(1, 11), 12)

# # Initialize a DataFrame filled with zeros
# df = pd.DataFrame(0, index=range(120), columns=columns)

# # Fill only diagonal cells with random values
# for i in range(120):
#     df.iloc[i, i] = np.random.rand()

# # Display the first 15 rows
# print(df.head(15))

# # Create the new 10x12 DataFrame with proper indexing
# df_rearranged = pd.DataFrame(0, index=[f"Year {y}" for y in range(1, 11)], columns=months)

# # Extract the diagonal values and reshape them into (10,12)
# diagonal_values = [df.iloc[i, i] for i in range(120)]  # Get diagonal values
# reshaped_values = np.array(diagonal_values).reshape(10, 12)  # Reshape into (10x12)

# # Assign values to the new DataFrame
# df_rearranged.iloc[:, :] = reshaped_values

# # Display the rearranged DataFrame
# print(df_rearranged)
