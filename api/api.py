from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import scraping.scraping as scraping
import json
from training.train_topic_model import run_training
from bertopic import BERTopic

app = FastAPI()
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "API is running!"}

@app.get("/titles/")
def read_titles():
    csv_file = "data/judul_penelitian.csv"
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
    json_file = "data/judul_penelitian.json"
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
    
@app.post("/train-topic-model/")
def train_topic_model_endpoint():
    try:
        run_training()
        return {"message": "Training berhasil!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/topics/")
def get_topics():
    try: 
        model_path = "models/bertopic_model"
        if not os.path.exists(model_path):
            raise HTTPException(status_code=404, detail="Model tidak ditemukan. Jalankan endpoint /train-topic-model terlebih dahulu.")
 
        topic_model = BERTopic.load(model_path)
 
        topics = topic_model.get_topics()
 
        topics_result = []
        for topic_id, words in topics.items():
            topics_result.append({
                "topic_id": topic_id,
                "words": [word for word, _ in words]
            })
        
        return {"topics": topics_result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
