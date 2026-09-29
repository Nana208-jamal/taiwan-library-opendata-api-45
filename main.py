import json
import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# 1. 資料庫連線 (SQLite)
DATABASE_URL = "sqlite:///./libraries.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. 定義資料表模型
class LibraryDB(Base):
    __tablename__ = "libraries"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    city = Column(String(50), index=True)         # 縣市 (基隆市, 臺北市...)
    name = Column(String(100), index=True)        # 圖書館名稱 (Name)
    area = Column(String(50), nullable=True)      # 行政區 (Area)
    address = Column(String(255), nullable=True)   # 地址 (Address)
    tel = Column(String(50), nullable=True)        # 電話 (TEL)
    url = Column(String(500), nullable=True)       # 官網連結 (URL)

Base.metadata.create_all(bind=engine)

# 3. Pydantic 驗證格式
class LibraryCreate(BaseModel):
    city: str
    name: str
    area: Optional[str] = None
    address: Optional[str] = None
    tel: Optional[str] = None
    url: Optional[str] = None

class LibraryResponse(LibraryCreate):
    id: int
    class Config:
        from_attributes = True

# 4. 初始化 FastAPI
app = FastAPI(
    title="全台公共圖書館 Open Data RESTful API",
    description="本服務將政府開放資料之圖書館資訊匯入 SQLite，並提供完整之標準 RESTful CRUD 操作端點。",
    version="1.0.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 啟動時自動解析你給的 data.json 巢狀結構並存入 SQLite
@app.on_event("startup")
def init_data():
    db = SessionLocal()
    if db.query(LibraryDB).count() == 0 and os.path.exists("data.json"):
        with open("data.json", "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            # 解析巢狀結構：[ {"縣市": "基隆市", "圖書館資訊": [...]}, ... ]
            for city_block in raw_data:
                city_name = city_block.get("縣市", "未分類")
                lib_list = city_block.get("圖書館資訊", [])
                for lib in lib_list:
                    item = LibraryDB(
                        city=city_name,
                        name=lib.get("Name", "未命名圖書館"),
                        area=lib.get("Area"),
                        address=lib.get("Address"),
                        tel=lib.get("TEL"),
                        url=lib.get("URL")
                    )
                    db.add(item)
            db.commit()
            print(">>> [Init] Open Data 已成功解析並匯入 SQLite 資料庫！")
    db.close()

# 5. RESTful CRUD 端點

# [Read All] 查詢清單 (支援依城市過濾 + 分頁)
@app.get("/api/v1/libraries", response_model=List[LibraryResponse], summary="取得圖書館清單 (Read All)")
def read_libraries(
    city: Optional[str] = Query(None, description="依縣市過濾，例如：臺北市"),
    skip: int = Query(0, ge=0, description="跳過筆數"),
    limit: int = Query(20, ge=1, le=100, description="取得筆數"),
    db: Session = Depends(get_db)
):
    query = db.query(LibraryDB)
    if city:
        query = query.filter(LibraryDB.city == city)
    return query.offset(skip).limit(limit).all()

# [Read Single] 依 ID 取得單筆資料
@app.get("/api/v1/libraries/{library_id}", response_model=LibraryResponse, summary="取得特定圖書館資料 (Read Single)")
def read_library(library_id: int, db: Session = Depends(get_db)):
    item = db.query(LibraryDB).filter(LibraryDB.id == library_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="找不到指定的圖書館資料")
    return item

# [Create] 新增一筆圖書館資料
@app.post("/api/v1/libraries", response_model=LibraryResponse, status_code=201, summary="新增圖書館資料 (Create)")
def create_library(payload: LibraryCreate, db: Session = Depends(get_db)):
    new_lib = LibraryDB(
        city=payload.city,
        name=payload.name,
        area=payload.area,
        address=payload.address,
        tel=payload.tel,
        url=payload.url
    )
    db.add(new_lib)
    db.commit()
    db.refresh(new_lib)
    return new_lib

# [Update] 修改指定圖書館資料
@app.put("/api/v1/libraries/{library_id}", response_model=LibraryResponse, summary="更新圖書館資料 (Update)")
def update_library(library_id: int, payload: LibraryCreate, db: Session = Depends(get_db)):
    item = db.query(LibraryDB).filter(LibraryDB.id == library_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="找不到指定的圖書館資料")
    
    item.city = payload.city
    item.name = payload.name
    item.area = payload.area
    item.address = payload.address
    item.tel = payload.tel
    item.url = payload.url
    
    db.commit()
    db.refresh(item)
    return item

# [Delete] 刪除指定圖書館資料
@app.delete("/api/v1/libraries/{library_id}", summary="刪除圖書館資料 (Delete)")
def delete_library(library_id: int, db: Session = Depends(get_db)):
    item = db.query(LibraryDB).filter(LibraryDB.id == library_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="找不到指定的圖書館資料")
    
    db.delete(item)
    db.commit()
    return {"message": f"ID {library_id} 的圖書館資料已成功刪除"}