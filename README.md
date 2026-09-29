# 🏛️ 全國公共圖書館資訊 RESTful API 服務系統

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688?style=for-the-badge&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)
![Swagger](https://img.shields.io/badge/Swagger-UI%20Enabled-85EA2D?style=for-the-badge&logo=swagger)

本專案運用政府資料開放平台（Open Data）之「全國公共圖書館資訊」資料集，結合 **FastAPI** 現代化高效能非同步框架與 **SQLite ORM (SQLAlchemy)**，實作一套符合業界規範的 RESTful API Server，提供完整的 CRUD 資料資源管理，並支援自動化 Swagger UI 互動文件與自動化測試客戶端。

---

## 📌 系統架構與特性

- **開放資料結構清洗**：原始資料為雙層巢狀 JSON 結構（縣市層級與分館陣列），伺服器啟動時自動解析並攤平持久化至 SQLite。
- **高標準 RESTful 路由架構**：符合 HTTP Method 動詞語意（`GET`, `POST`, `PUT`, `DELETE`）與標準狀態碼（`200 OK`, `201 Created`, `404 Not Found`）。
- **強型別驗證**：全面導入 `Pydantic` 進行 Request Body 結構驗證與 Response Schema 序列化過濾。
- **即時互動文件**：FastAPI 原生 OpenAPI / Swagger UI 支援，零設定自動生成線上文件。

---

## 📂 專案檔案結構

```text
├── data.json              # 原始開放資料集 (全國公共圖書館資料)
├── libraries.db           # SQLite 關聯式資料庫檔 (系統啟動時自動建置)
├── main.py                # FastAPI 核心服務程式 (含 ORM 宣告、DB 匯入與 CRUD 路由)
├── test_client.py         # Python 自動化 API 測試客戶端 (驗證完整生命週期)
├── requirements.txt       # 專案相依環境清單
├── swagger_ui.png         # Swagger UI 線上互動文件截圖
├── test_result.png        # 測試腳本自動化執行成果截圖
└── README.md              # 系統開發與維運說明文件