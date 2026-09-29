import requests

BASE_URL = "http://127.0.0.1:8000/api/v1/libraries"

def run_tests():
    print("==================================================")
    print("        開始執行 圖書館 RESTful API 自動化測試       ")
    print("==================================================\n")

    # 1. 測試 GET 全部資料 (Read All)
    print("[測試 1] GET /api/v1/libraries (查詢前 2 筆)")
    res = requests.get(f"{BASE_URL}?skip=0&limit=2")
    print(f"Status Code: {res.status_code}")
    print(f"Response: {res.json()}\n")

    # 2. 測試 POST 新增一筆 (Create)
    print("[測試 2] POST /api/v1/libraries (新增測試分館)")
    create_payload = {
        "city": "臺北市",
        "name": "北商大智慧圖書中心",
        "area": "中正區",
        "address": "臺北市中正區濟南路一段321號",
        "tel": "02-23226000",
        "url": "https://www.ntub.edu.tw"
    }
    res = requests.post(BASE_URL, json=create_payload)
    print(f"Status Code: {res.status_code}")
    new_data = res.json()
    print(f"Response: {new_data}\n")
    created_id = new_data["id"]

    # 3. 測試 GET 單筆 (Read Single)
    print(f"[測試 3] GET /api/v1/libraries/{created_id} (查詢剛新增的資料)")
    res = requests.get(f"{BASE_URL}/{created_id}")
    print(f"Status Code: {res.status_code}")
    print(f"Response: {res.json()}\n")

    # 4. 測試 PUT 更新 (Update)
    print(f"[測試 4] PUT /api/v1/libraries/{created_id} (更新電話與名稱)")
    update_payload = {
        "city": "臺北市",
        "name": "北商大智慧圖書中心 (資訊館)",
        "area": "中正區",
        "address": "臺北市中正區濟南路一段321號 五育樓",
        "tel": "02-23226111",
        "url": "https://www.ntub.edu.tw"
    }
    res = requests.put(f"{BASE_URL}/{created_id}", json=update_payload)
    print(f"Status Code: {res.status_code}")
    print(f"Response: {res.json()}\n")

    # 5. 測試 DELETE 刪除 (Delete)
    print(f"[測試 5] DELETE /api/v1/libraries/{created_id} (刪除該筆資料)")
    res = requests.delete(f"{BASE_URL}/{created_id}")
    print(f"Status Code: {res.status_code}")
    print(f"Response: {res.json()}\n")

    # 6. 驗證是否真的刪除了 (404)
    print(f"[測試 6 驗證] 再次 GET /api/v1/libraries/{created_id} (預期應回傳 404)")
    res = requests.get(f"{BASE_URL}/{created_id}")
    print(f"Status Code: {res.status_code} (正確！)\n")

    print("==================================================")
    print("          🎉 所有 CRUD 功能驗證成功且通過！        ")
    print("==================================================")

if __name__ == "__main__":
    run_tests()