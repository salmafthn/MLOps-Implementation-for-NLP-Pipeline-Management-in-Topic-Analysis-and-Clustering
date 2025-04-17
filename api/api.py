from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import scraping
import json

app = FastAPI()

# Tambahkan CORS agar bisa diakses dari frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Bisa disesuaikan dengan kebutuhan frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "API is running!"}

@app.get("/titles/")
def read_titles():
    csv_file = "judul_penelitian.csv"
    if not os.path.exists(csv_file):
        raise HTTPException(status_code=404, detail="File CSV tidak ditemukan. Jalankan endpoint /scrape terlebih dahulu.")

    try:
        df = pd.read_csv(csv_file)
        if "title" not in df.columns:
            raise HTTPException(status_code=500, detail="Kolom 'title' tidak ditemukan dalam file CSV.")
        return {"titles": df["title"].dropna().tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/data/")
def get_full_data():
    json_file = "judul_penelitian.json"
    if not os.path.exists(json_file):
        raise HTTPException(status_code=404, detail="File JSON tidak ditemukan. Jalankan endpoint /scrape terlebih dahulu.")

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scrape/")
def run_scraping():
    try:
        scraping.scrape_titles()
        return {"message": "Scraping selesai, data diperbarui dan disimpan ke CSV & JSON."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
