#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import csv
from datetime import date
import shutil
import os

def download_and_process_twse_csv(date: str) -> str:
    """
    Downloads the TWSE CSV file for a specified date and processes it to remove
    the first line and empty lines, saving the original and processed formats.

    Returns the path of the processed output file.

    :param date: Date in 'YYYYMMDD' format.
    :return: The path to the processed CSV file.
    """
    base_url = "https://www.twse.com.tw/exchangeReport/BWIBBU_d"
    params = {
        "response": "csv",
        "date": date,
        "selectType": "ALL"
    }

    try:
        # Send the GET request
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Save the raw CSV file in the "raw" folder
        raw_folder = "raw"
        os.makedirs(raw_folder, exist_ok=True)
        raw_file = os.path.join(raw_folder, f"TWSE_{date}.csv")
        with open(raw_file, "w", encoding="utf-8") as raw_csv_file:
            raw_csv_file.write(response.text)

        print(f"Raw file saved as: {raw_file}")

        # Split response text into lines and process
        lines = response.text.splitlines()

        # Remove the first line (title) and any empty lines
        processed_lines = [line for line in lines[1:] if line.strip()]

        # Preprocess lines to remove nested quotes, normalize fields, and handle commas in numbers
        normalized_lines = []
        for line in processed_lines:
            fields = next(csv.reader([line]))
            normalized_fields = [field.replace(",", "") for field in fields]  # Remove commas in numeric fields
            normalized_lines.append(normalized_fields)

        # Write processed data to a new CSV file with minimal quoting
        processed_output_file = f"TWSE_{date}.csv"
        with open(processed_output_file, "w", encoding="utf-8", newline='') as processed_file:
            writer = csv.writer(processed_file, quoting=csv.QUOTE_MINIMAL)
            writer.writerows(normalized_lines)

        print(f"Processed file saved as: {processed_output_file}")
        return processed_output_file
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return ""

# Main execution
#processed_output_file = download_and_process_twse_csv("20241220")
today = date.today().strftime("%Y%m%d")
processed_output_file = download_and_process_twse_csv(today)

# Check if the file exists and is not empty before copying
if processed_output_file and os.path.exists(processed_output_file) and os.path.getsize(processed_output_file) > 0:
    shutil.copy(processed_output_file, "TWSE.csv")
    print(f"Processed CSV has also been copied to 'TWSE.csv'.")
else:
    print("No file to copy due to an error in processing or the file is empty.")
