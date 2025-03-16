import pandas as pd

url = "https://raw.githubusercontent.com/salmafthn/MLOps-Implementation-for-NLP-Pipeline-Management-in-Topic-Analysis-and-Clustering/main/judul_penelitian.csv"

# Load dataset dari file yang telah diunduh
data = pd.read_csv(url)

# Menampilkan 5 baris pertama
data.head()

# Informasi dataset
data.info()

# Statistik panjang teks
data["text_length"] = df["Judul Penelitian"].apply(len)
data["word_count"] = df["Judul Penelitian"].apply(lambda x: len(x.split()))

# Menampilkan statistik dasar
data[["text_length", "word_count"]].describe()