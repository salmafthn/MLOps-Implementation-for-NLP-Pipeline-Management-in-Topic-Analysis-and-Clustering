import os
import pandas as pd
import shutil
from bertopic import BERTopic
from training.evaluate_topic_model import evaluate_coherence  # <--- Import evaluasi

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
    # Cek apakah path adalah direktori dan pastikan foldernya tidak kosong
    if os.path.exists(save_path) and os.path.isdir(save_path):
        # Coba hapus folder jika tidak terkunci
        try:
            shutil.rmtree(save_path)
        except Exception as e:
            print(f"Error menghapus folder {save_path}: {e}")
            pass  # Jika gagal, lanjutkan saja tanpa menghapus

def run_training():
    docs = load_data()
    topic_model = BERTopic(language="english", verbose=True)
    topics, probs = topic_model.fit_transform(docs)

    # Path absolut untuk folder model (menggunakan os.path.abspath untuk memastikan path yang benar)
    base_path = os.path.abspath("models")
    save_path = os.path.join(base_path, "bertopic_model")
    
    # Pastikan folder models sudah ada
    os.makedirs(base_path, exist_ok=True)

    # Dapatkan coherence score untuk model lama (jika ada)
    old_coherence_score = get_old_coherence_score(save_path, docs)

    # Evaluasi coherence score untuk model baru
    new_coherence_score = evaluate_coherence(topic_model, docs)
    print(f"Coherence Score Baru: {new_coherence_score}")

    # Jika coherence score baru lebih tinggi dari yang lama, overwrite model
    if old_coherence_score is None or new_coherence_score > old_coherence_score:
        # Bersihkan direktori model lama terlebih dahulu dengan aman
        clean_directory(save_path)
        topic_model.save(save_path)
        print("Model baru disimpan, karena memiliki coherence score lebih tinggi.")
    else:
        print("Coherence score baru tidak lebih tinggi, model tidak di-overwrite.")
