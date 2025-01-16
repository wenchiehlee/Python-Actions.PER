import requests
import csv
import logging
import sys
import json
import os
from datetime import datetime

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# API URLs 和 Headers
APIS = {
    "TWSE": "https://openapi.twse.com.tw/v1/exchangeReport/BWIBBU_d",
    "TPEX": "https://www.tpex.org.tw/openapi/v1/tpex_mainboard_peratio_analysis"
}

HEADERS = {
    "accept": "application/json",
    "If-Modified-Since": "Mon, 26 Jul 1997 05:00:00 GMT",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}

# 繁體中文欄位名稱
STANDARD_HEADERS_ZH = [
    "財務年度季度", "公司代號", "公司名稱", 
    "本益比", "每股股利", "殖利率", "股價淨值比"
]

def fetch_api_data(api_url, headers):
    """從 API 獲取資料"""
    try:
        logging.info(f"正在從 API 獲取資料：{api_url}")
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # 檢查 HTTP 錯誤
        data = response.json()  # 解析 JSON 響應
        logging.info(f"成功從 API 獲取 {len(data)} 筆記錄。")
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP 錯誤發生：{e}")
    except Exception as e:
        logging.error(f"發生錯誤：{e}")
    return []

def map_tpex_to_standard_zh(data):
    """映射 TPEX 資料到繁體中文格式"""
    return {
        "財務年度季度": data.get("Date"),
        "公司代號": data.get("SecuritiesCompanyCode"),
        "公司名稱": data.get("CompanyName"),
        "本益比": data.get("PriceEarningRatio"),
        "每股股利": data.get("DividendPerShare"),
        "殖利率": data.get("YieldRatio"),
        "股價淨值比": data.get("PriceBookRatio")
    }

def map_twse_to_standard_zh(data):
    """映射 TWSE 資料到繁體中文格式"""
    return {
        "財務年度季度": data.get("FiscalYearQuarter"),
        "公司代號": data.get("Code"),
        "公司名稱": data.get("Name"),
        "本益比": data.get("PEratio"),
        "每股股利": None,  # TWSE 沒有這個欄位
        "殖利率": data.get("DividendYield"),
        "股價淨值比": data.get("PBratio")
    }

def write_standardized_data_to_csv(json_data, csv_file, headers, mapping_func, mode='w'):
    """寫入標準化的 CSV 資料（繁體中文）"""
    if not json_data:
        logging.error("沒有資料可寫入 CSV。")
        return

    mapped_data = [mapping_func(item) for item in json_data]
    try:
        with open(csv_file, mode=mode, encoding='utf-8-sig', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            if mode == 'w':  # 如果是覆寫模式，寫入標題
                writer.writeheader()
            writer.writerows(mapped_data)
        logging.info(f"標準化資料已成功寫入 {csv_file}。")
    except Exception as e:
        logging.error(f"寫入標準化資料至 CSV 失敗：{e}")

def write_summary_json(file_name, label, message):
    """寫入摘要 JSON 文件"""
    summary = {
        "schemaVersion": 1,
        "label": label,
        "message": str(message),
        "color": "blue"
    }
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(summary, file, ensure_ascii=False, indent=4)
        logging.info(f"摘要 JSON 已成功寫入 {file_name}。")
    except Exception as e:
        logging.error(f"寫入摘要 JSON 失敗：{e}")

def main():
    # 預設輸出文件名
    today_str = datetime.now().strftime("%Y%m%d")
    default_csv = f"歷史資料/{today_str}.csv"
    backup_csv = "TWSE_TPEX.csv"

    # 檢查命令列參數
    if len(sys.argv) == 2:
        output_csv = sys.argv[1]
    else:
        logging.info(f"未指定輸出文件，將使用預設文件名：{default_csv}")
        output_csv = default_csv

    # 創建輸出目錄（如有需要）
    output_dir = os.path.dirname(output_csv)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # 迭代每個 API，獲取資料並寫入 CSV
    for api_name, api_url in APIS.items():
        logging.info(f"處理 API：{api_name}")
        data = fetch_api_data(api_url, HEADERS)
        write_mode = 'w' if api_name == "TWSE" else 'a'  # 第一個 API 覆寫，後續追加
        mapping_func = map_tpex_to_standard_zh if api_name == "TPEX" else map_twse_to_standard_zh
        write_standardized_data_to_csv(data, output_csv, STANDARD_HEADERS_ZH, mapping_func, mode=write_mode)

        # 寫入備份文件
        write_standardized_data_to_csv(data, backup_csv, STANDARD_HEADERS_ZH, mapping_func, mode=write_mode)

        # 寫入摘要 JSON 文件
        summary_file_name = f"{api_name.replace(' ', '_')}.json"
        write_summary_json(summary_file_name, f"{api_name} 公司數", len(data))

if __name__ == "__main__":
    main()
