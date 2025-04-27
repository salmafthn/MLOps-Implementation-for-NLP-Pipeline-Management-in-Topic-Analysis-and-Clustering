import os
import pandas as pd
import shutil
import json
from bertopic import BERTopic
from training.evaluate_topic_model import evaluate_coherence 

def load_data():
    data_path = "data/judul_penelitian.csv"
    df = pd.read_csv(data_path)
    df = df.dropna(subset=['title', 'abstract'])
    df['text'] = df['title'] + ". " + df['abstract']
    return df['text'].tolist()

def get_old_coherence_score(model_path, docs):
    """Mengambil coherence score dari model lama jika ada"""
    if os.path.exists(model_path):
        topic_model = BERTopic.load(model_path)
        return evaluate_coherence(topic_model, docs)
    else:
        return None

def clean_directory(save_path):
    """Membersihkan folder dan memastikan folder dapat dihapus dengan aman"""
    if os.path.exists(save_path) and os.path.isdir(save_path):
        try:
            shutil.rmtree(save_path)
        except Exception as e:
            print(f"Error menghapus folder {save_path}: {e}")
            pass 

def run_training():
    docs = load_data()
    topic_model = BERTopic(language="english", verbose=True)
    topics, probs = topic_model.fit_transform(docs)

    base_path = os.path.abspath("models")
    save_path = os.path.join(base_path, "bertopic_model")
    
    os.makedirs(base_path, exist_ok=True)

    old_coherence_score = get_old_coherence_score(save_path, docs)

    new_coherence_score = evaluate_coherence(topic_model, docs)
    print(f"Coherence Score Baru: {new_coherence_score}")

    if old_coherence_score is None or new_coherence_score > old_coherence_score:
        clean_directory(save_path)
        topic_model.save(save_path)
        print("Model baru disimpan, karena memiliki coherence score lebih tinggi.")
    else:
        print("Coherence score baru tidak lebih tinggi, model tidak di-overwrite.")

    # Simpan hasil untuk dikonsumsi script lain
    with open("results.json", "w") as f:
        json.dump({
            "coherence_score": new_coherence_score,
            "docs_size": len(docs),
            "topics": topics
        }, f)

if __name__ == "__main__":
    run_training()
