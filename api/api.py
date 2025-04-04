from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import scraping
import requests

app = FastAPI()

# Tambahkan CORS agar bisa diakses dari frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Bisa diganti dengan domain tertentu jika perlu
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
        raise HTTPException(status_code=404, detail="File CSV tidak ditemukan. Jalankan scrapping.py dulu.")

    try:
        df = pd.read_csv(csv_file)
        return {"titles": df["Judul Penelitian"].tolist()}
    except Exception as e:
        return {"error": str(e)}

# **Tambahkan Endpoint untuk Scraping**
@app.post("/scrape")
def run_scraping():
    try:
        scraping.scrape_titles()
        return {"message": "Scraping selesai, data diperbarui!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
