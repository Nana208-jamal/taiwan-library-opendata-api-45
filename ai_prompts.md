# 🤖 AI 輔助開發紀錄與設定說明 (AI Prompts & Workflow Log)

本專案於規劃、架構設計、資料處理與測試腳本開發過程中，導入生成式 AI 輔助開發工具（Gemini / ChatGPT），以下為關鍵階段之提示詞（Prompt Engineering）與成果產出紀錄。

---

## 一、階段一：系統架構與 RESTful API 規格規劃
- **使用工具**：Gemini
- **主要提示詞 (Prompt)**：
  > 「我需要使用 Python + FastAPI 與 SQLite 實作一套完整的 RESTful API Server，請針對台灣公共圖書館的 Open Data 規劃標準的 CRUD 端點，必須符合 HTTP Method 動詞語意（GET, POST, PUT, DELETE），並支援分頁與特定欄位篩選。」
- **AI 產出與採納**：
  - 規劃出符合 RESTful 規範的端點路徑（`/api/v1/libraries`）。
  - 建議採用 SQLAlchemy ORM 進行 SQLite 資料持久化，避免手寫原生 SQL 造成注入風險。

---

## 二、階段二：非扁平巢狀 JSON 資料清洗與匯入
- **使用工具**：Gemini
- **主要提示詞 (Prompt)**：
  > 「我的 Open Data 原始資料是雙層巢狀結構（外層為縣市名稱，內層為圖書館清單陣列），欄位包含 Name、Address、TEL、Area 等。請幫我設計在 FastAPI 啟動時自動解析此 JSON 並將資料攤平匯入 SQLite 的邏輯。」
- **AI 產出與採納**：
  - 設計 `@app.on_event("startup")` 啟動事件鉤子。
  - 實作雙層迴圈解析邏輯，成功將巢狀結構平鋪映射至 `libraries` 資料表。

---

## 三、階段三：Pydantic Schema 與強型別驗證
- **使用工具**：Gemini
- **主要提示詞 (Prompt)**：
  > 「請為上述圖書館資料設計 Pydantic 模型，包含新增用的 LibraryCreate 以及回傳用的 LibraryResponse，需要自動包含自增 ID，且部分欄位如電話或網址需支援 Optional。」
- **AI 產出與採納**：
  - 建立嚴謹的型別驗證模型，確保客戶端傳入資料時能自動檢核，錯誤時自動回傳 422 狀態碼。

---

## 四、階段四：自動化測試客戶端開發
- **使用工具**：Gemini
- **主要提示詞 (Prompt)**：
  > 「請使用 Python Requests 函式庫撰寫一支自動化測試腳本 test_client.py，依序測試：讀取全部、新增單筆、讀取該單筆、更新單筆、刪除單筆，最後再次讀取確認回傳 404 Not Found。」
- **AI 產出與採納**：
  - 自動化完整生命週期測試程式碼，執行後於終端機印出各步驟狀態碼與回傳內容，便於驗收截圖。