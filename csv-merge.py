#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd

# List of file paths
file_paths = [
    "TWSE.csv",
    "TPEX.csv"
]

# Initialize an empty list to store processed DataFrames
dataframes = []

for file in file_paths:
    # Read the CSV file
    df = pd.read_csv(file)
    
    # Drop completely empty columns
    df = df.dropna(axis=1, how="all")
    
    # Drop columns with names starting with 'Unnamed'
    df = df.loc[:, ~df.columns.str.contains('^Unnamed', na=False)]
    
    # Append the cleaned DataFrame to the list
    dataframes.append(df)

# Combine all cleaned DataFrames
merged_data = pd.concat(dataframes, ignore_index=True)

# Save the merged data to a new CSV file
merged_data.to_csv("TWSE_TPEX.csv", index=False)

print("Data merged and saved as 'TWSE_TPEX.csv'")
