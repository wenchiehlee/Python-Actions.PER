#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import pandas as pd
from datetime import date
import os
import shutil

def download_and_process_tpex_csv(date_str):
    """
    Download and process the TPEx CSV file for a given date.

    Args:
        date_str (str): The date in YYYYMMDD format.

    Returns:
        tuple: The names of the processed output file and the downloaded raw file.
    """
    # Convert the date format to the required format (YYYY/MM/DD)
    formatted_date = f"{date_str[:4]}/{date_str[4:6]}/{date_str[6:]}"
    
    # TPEx URL for downloading the CSV
    url = (
        f"https://www.tpex.org.tw/web/stock/aftertrading/peratio_analysis/"
        f"pera_result.php?l=zh-tw&o=csv&d={formatted_date}&c=&s=0,asc"
    )

    # Fetch the CSV file
    response = requests.get(url)
    response.encoding = 'big5'  # Set encoding to BIG5 for TPEx CSV

    # Check if the request was successful
    if response.status_code != 200:
        raise ValueError(f"Failed to download data. Status code: {response.status_code}")

    # Save a copy of the downloaded file in the 'raw' folder
    raw_folder = "raw"
    os.makedirs(raw_folder, exist_ok=True)
    raw_file = os.path.join(raw_folder, f"TPEX_{date_str}.csv")
    with open(raw_file, "w", encoding="utf-8") as file:
        file.write(response.text)

    # Load the data into a pandas DataFrame
    try:
        df = pd.read_csv(raw_file, skiprows=6, on_bad_lines="skip", encoding="utf-8")  # Skip metadata rows
    except pd.errors.EmptyDataError:
        raise ValueError("The downloaded file is empty or not valid CSV format.")

    # Rename columns to standard headers
    expected_headers = [
        "證券代號", "證券名稱", "本益比", "每股股利(註)", 
        "股利年度", "殖利率(%)", "股價淨值比"
    ]
    if len(df.columns) >= len(expected_headers):
        df.columns = expected_headers

    # Add missing columns
    additional_columns = ["收盤價", "財報年/季"]
    for col in additional_columns:
        if col not in df.columns:
            df[col] = None  # Add as empty column

    # Reorder columns to match the desired order
    desired_order = [
        "證券代號", "證券名稱", "收盤價", "殖利率(%)", "股利年度", 
        "本益比", "股價淨值比", "財報年/季", "每股股利(註)"
    ]
    df = df.reindex(columns=desired_order)

    # Trim trailing spaces in the "證券名稱" column
    if "證券名稱" in df.columns:
        df["證券名稱"] = df["證券名稱"].astype(str).str.strip()

    # Save processed data to the main folder
    processed_file = f"TPEX_{date_str}.csv"
    with open(processed_file, "w", encoding="utf-8-sig") as file:
        if not df.empty:
            file.write(",".join(desired_order) + ",\n")  # Write header with trailing comma
            for _, row in df.iterrows():
                row_data = [str(item) if pd.notna(item) else "" for item in row]
                file.write(",".join(row_data) + ",\n")  # Write rows with trailing comma

    return processed_file, raw_file

# Example usage
if __name__ == "__main__":
    today = date.today().strftime("%Y%m%d")
    try:
        processed_output_file, raw_file = download_and_process_tpex_csv("today")
        print(f"Raw file saved as: {raw_file}")
        print(f"Processed file saved as: {processed_output_file}")
    except ValueError as e:
        print(f"Error: {e}")

# Check if the file exists and is not empty before copying
if processed_output_file and os.path.exists(processed_output_file) and os.path.getsize(processed_output_file) > 0:
    shutil.copy(processed_output_file, "TPEX.csv")
    print(f"Processed CSV has also been copied to 'TPEX.csv'.")
else:
    print("No file to copy due to an error in processing or the file is empty.")