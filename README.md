[![OpenAPI On GitHub Actions](https://github.com/wenchiehlee/Python-Actions.PER/actions/workflows/Actions.yaml/badge.svg)](https://github.com/wenchiehlee/Python-Actions.PER/actions/workflows/Actions.yaml)

![Endpoint Badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/wenchiehlee/Python.TWSE-PER/main/TWSE.json)
![Endpoint Badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/wenchiehlee/Python.TWSE-PER/main/TPEX.json)⟶[![Endpoint Badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/wenchiehlee/Python.TWSE-PER/main/TWSE_TPEX.json)](TWSE_TPEX.csv)

# Python-Actions.PER
Working space for Python-Actions.PER

There are two ways to get PER data of TWSE and TPEX stock. One is OpenAPI, one is web download.
## The PER data based on OpenAPI
  * [盤後資訊 > 上市個股日本益比、殖利率及股價淨值比（依代碼查詢） (臺灣證券交易所)](https://data.gov.tw/dataset/11547)
      *  API: https://openapi.twse.com.tw/v1/exchangeReport/BWIBBU_d including historical PER
  * [盤後資訊 >上櫃股票個股本益比、殖利率、股價淨值比](https://data.gov.tw/dataset/11373)
      *  API: https://www.tpex.org.tw/openapi/v1/tpex_mainboard_peratio_analysis 

## The PER data based on web download
  * TWSE PER (including historical PER)
    * https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=html&date=20220701&selectType=ALL
  * TPEX PER (including historical PER)
    * https://www.tpex.org.tw/web/stock/aftertrading/peratio_analysis/pera_result.php?l=zh-tw&o=htm&d=111/07/01&c=&s=0,asc

## 投資參考資料計算說明

### 重點摘要

#### 1. **本益比 (Price-to-Earnings Ratio, P/E)**
- **計算公式**：`收盤價 / 每股參考稅後純益`
- 每股參考稅後純益計算基礎：
  - `公司稅後純益 / 發行參考股數`
- 特別說明：
  - 當每股參考稅後純益為 0 或負數時，**不計算本益比**。
  - 使用的稅後純益數據來自上市公司於公開資訊觀測站申報的**最近四季財務報告**。

---

#### 2. **殖利率 (Dividend Yield)**
- **計算公式**：`(每股股利 / 收盤價) × 100%`
- 每股股利計算基礎包含：
  - **現金股利**（元/股）。
  - **法定盈餘公積**與**資本公積**的現金發放（元/股）。
  - **盈餘轉增資股票股利**（元/股）。

---

#### 3. **股價淨值比 (Price-to-Book Ratio, P/B)**
- **計算公式**：`收盤價 / 每股參考淨值`
- 每股參考淨值的基礎來自：
  - 公開資訊觀測站公告的**最近一季淨值**。

---

### 推計基礎與特殊說明
1. 若上市公司為新設公司，計算方式以該公司**申報資料**為基礎。
   - 例如：新公司設立未滿一年時，僅使用自設立以來的數據。
2. 本頁面資料**不包含即時數據**，僅參考已申報的歷史資料。
3. 若當日無收盤價，將依公司內部規則決定**替代價格**。

---

### 注意事項
- 資料僅供**研究參考**，**不應視為投資建議**。
- 股利與財報資訊自**民國 106 年（西元 2017 年）**起提供。
- 股票名稱若附註「`*`」，表示每股面額非新台幣 10 元，其計算方式已調整。

---

## 限制與例外
1. 若公司未申報完整財務報告或資料不齊全，則不計算相關指標。
2. 所有資料以**公開資訊觀測站公告**為基礎。
3. 計算時未包含**回溯調整**。

---

以上說明針對**本益比**、**殖利率**及**股價淨值比**的計算方式與邏輯提供清晰解釋，適合研究台股指標的投資者參考，**但不可作為直接投資依據**。

# Python-Actions.IssueShares (已發行普通股數)
