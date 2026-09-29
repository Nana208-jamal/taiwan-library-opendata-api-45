# Taiwan Public Libraries Information RESTful API

以文化部「全國公共圖書館資訊」Open Data 為基礎，使用 Python、FastAPI、SQLAlchemy 與 SQLite 實作 RESTful API Server。  
本專案提供完整 CRUD 操作，並支援依縣市（City）篩選與分頁查詢。FastAPI 會自動產生 Swagger UI API 文件，專案內亦附帶 Python API Client，可直接測試各項 RESTful APIs。

---

## 1. Open Data

本專案使用政府資料開放平台「全國公共圖書館資訊」Open Data。  
原始資料存放於：
`data.json`

原始開放資料為雙層巢狀結構（縣市層級包覆圖書館資訊清單），系統啟動時會透過解析邏輯自動將資料平鋪寫入 SQLite Database，再由 FastAPI 提供 RESTful API 存取。

### 資料欄位對照說明

| 原始欄位 | API / Database 欄位 | 型態 | 說明 |
| :--- | :--- | :--- | :--- |
| - | `id` | Integer | 資料庫主鍵 (Primary Key, Auto Increment) |
| 縣市 | `city` | String | 所屬縣市（如：基隆市、臺北市、新北市） |
| Name | `name` | String | 圖書館名稱 |
| Area | `area` | String | 行政區（如：中正區、大安區） |
| Address | `address` | String | 圖書館詳細地址 |
| TEL | `tel` | String | 連絡電話 |
| URL | `url` | String | 圖書館官方網站連結 |

---

## 2. Technology

本專案使用以下技術與工具建置：
- **Python 3.10+**
- **FastAPI**：高效能非同步 Web 框架
- **SQLAlchemy**：ORM 資料庫映射工具
- **SQLite**：輕量化關聯式資料庫
- **Pydantic**：Request / Response 資料綱要驗證
- **Requests**：客戶端 HTTP 請求測試工具
- **Uvicorn**：ASGI 伺服器
- **Swagger UI**：自動產生互動式 API 文件

---

## 3. Project Structure

```text
open_data_api/
├── data.json              # 原始開放資料 (Open Data JSON)
├── libraries.db           # SQLite Database (啟動時自動生成)
├── main.py                # FastAPI 核心應用、資料庫模型與 CRUD 路由
├── test_client.py         # Python 自動化 API Client 測試腳本
├── requirements.txt       # 專案相依套件清單
├── swagger_ui.png         # Swagger UI 文件截圖
├── test_result.png        # 測試腳本執行結果截圖
└── README.md              # 專案技術說明文件