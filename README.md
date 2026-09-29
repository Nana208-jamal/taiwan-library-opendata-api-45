# 🏛️ Taiwan Public Libraries RESTful API Hub

<p align="left">
  <img src="[https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)" />
  <img src="[https://img.shields.io/badge/FastAPI-0.110.0-009688?style=for-the-badge&logo=fastapi&logoColor=white](https://img.shields.io/badge/FastAPI-0.110.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)" />
  <img src="[https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)" />
  <img src="[https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)" />
  <img src="[https://img.shields.io/badge/Swagger-UI%20Interactive-85EA2D?style=for-the-badge&logo=swagger&logoColor=black](https://img.shields.io/badge/Swagger-UI%20Interactive-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)" />
</p>

> 以政府開放資料（Open Data）為基礎，透過現代化後端架構與 AI 輔助開發，打造支援結構化解析、全功能 CRUD 與高親和性 Swagger 互動文件的公共圖書館資訊服務系統。

---

## 💡 專案亮點與核心特色 (Highlights)

- **自動化巢狀資料清洗**：原始資料為非扁平的「縣市-分館陣列」雙層結構，系統於啟動時自動解析、正規化並持久化寫入 SQLite 資料庫。
- **高標準語意化 RESTful 設計**：精確匹配 HTTP Method（`GET` / `POST` / `PUT` / `DELETE`）與狀態碼機制（`200 OK`、`201 Created`、`404 Not Found`）。
- **多維度檢索與分頁**：支援 `?city=` 縣市過濾，結合 `skip` 與 `limit` 分頁參數，解決大規模資料傳輸效能問題。
- **型別安全與自動文件**：透過 Pydantic Schema 實現請求與回應的強型別驗證，內建零設定的 OpenAPI / Swagger UI 規格文件。

---

## 1. 📂 Open Data 資料架構

本專案採用政府資料開放平台「全國公共圖書館資訊」Open Data。  
原始資料集：`data.json`

### 欄位正規化對照表

| 原始資料欄位 | 資料庫 / API 欄位 | 型態 | 欄位說明 | 範例資料 |
| :--- | :--- | :--- | :--- | :--- |
| *(Auto Gen)* | `id` | Integer | 唯一識別碼 (Primary Key) | `1` |
| 縣市 | `city` | String | 所屬縣市 | `臺北市` |
| Name | `name` | String | 圖書館名稱 | `臺北市立圖書館總館` |
| Area | `area` | String | 所屬行政區 | `大安區` |
| Address | `address` | String | 據點詳細地址 | `臺北市大安區建國南路二段125號` |
| TEL | `tel` | String | 連絡電話 | `02-27552823` |
| URL | `url` | String | 官方資訊連結 | `[https://tpml.gov.taipei/](https://tpml.gov.taipei/)` |

---

## 2. 🛠️ 專案檔案結構 (Project Structure)

```text
open_data_api/
├── data.json              # 原始開放資料 (Open Data JSON)
├── libraries.db           # SQLite 關聯式資料庫 (系統自動生成)
├── main.py                # FastAPI 核心服務、ORM 與 CRUD 路由
├── test_client.py         # Python 自動化 API Client 測試腳本
├── requirements.txt       # 相依環境套件清單
├── ai_prompts.md          # AI 輔助開發過程紀錄檔
├── swagger_ui.png         # Swagger UI 文件執行截圖
├── test_result.png        # 自動化測試客戶端執行結果截圖
└── README.md              # 系統技術規格與說明文件

🚀 執行方式
1. 安裝套件Bashpip install -r requirements.txt
2. 啟動 API ServerBashuvicorn main:app --reload
3. 開啟 Swagger UI開啟瀏覽器直接造訪：👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
4. 執行 API Client 測試保持 Server 運行，開啟另一終端機視窗執行：Bashpython test_client.py


## 📡 API Endpoints
| Method | Endpoint | 功能 |
|---|---|---|
| GET | /api/v1/libraries | 查詢圖書館清單 |
| GET | /api/v1/libraries/{id} | 查詢單筆資料 |
| POST | /api/v1/libraries | 新增圖書館 |
| PUT | /api/v1/libraries/{id} | 修改圖書館 |
| DELETE | /api/v1/libraries/{id} | 刪除圖書館 |