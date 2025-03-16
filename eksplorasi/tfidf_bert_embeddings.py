from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer

# Inisialisasi TF-IDF
vectorizer = TfidfVectorizer(max_features=500)
tfidata_matrix = vectorizer.fit_transform(data["Judul Penelitian"])

# Konversi ke DataFrame
tfidf_data = pd.DataFrame(tfidata_matrix.toarray(), columns=vectorizer.get_feature_names_out())
tfidf_data.head()

# Load model BERT
model = SentenceTransformer("all-MiniLM-L6-v2")

# Encode teks ke dalam bentuk embeddings
bert_embeddings = model.encode(data["Judul Penelitian"], show_progress_bar=True)

# Menampilkan ukuran embeddings
bert_embeddings.shape