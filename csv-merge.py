#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd

# List of file paths
file_paths = [
    "TWSE.csv",
    "TPEX.csv"
]

# Load and combine all CSV files
dataframes = [pd.read_csv(file) for file in file_paths]
merged_data = pd.concat(dataframes, ignore_index=True)

# Save the merged data to a new CSV file
merged_data.to_csv("TWSE_TPEX.csv", index=False)

print("Data merged and saved as 'TWSE_TPEX.csv'")