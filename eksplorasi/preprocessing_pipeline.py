from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer

def load_data(url):
    data = pd.read_csv(url)
    return data

def preprocess_text(data):
    data["text_length"] = data["Judul Penelitian"].apply(len)
    data["word_count"] = data["Judul Penelitian"].apply(lambda x: len(x.split()))
    return data

def generate_wordcloud(data):
    text_corpus = " ".join(data["Judul Penelitian"])
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text_corpus)
    
    # Tampilkan WordCloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("WordCloud dari Judul Penelitian")
    plt.show()

def get_tfidata_features(texts):
    vectorizer = TfidfVectorizer(max_features=500)
    return vectorizer.fit_transform(texts), vectorizer.get_feature_names_out()

def get_bert_embeddings(texts):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(texts)

if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/salmafthn/MLOps-Implementation-for-NLP-Pipeline-Management-in-Topic-Analysis-and-Clustering/main/judul_penelitian.csv"
    
    print("Memuat dataset...")
    data = load_data(url)
    data = preprocess_text(data)

    print("\nStatistik dasar dataset:")
    print(data[["text_length", "word_count"]].describe())

    print("\nMembuat WordCloud...")
    generate_wordcloud(data)

    print("\nMenghasilkan TF-IDF representation...")
    tfidata_matrix, feature_names = get_tfidata_features(data["Judul Penelitian"])
    print("Fitur TF-IDF:", feature_names[:10])

    print("Menghasilkan BERT embeddings...")
    bert_embeddings = get_bert_embeddings(data["Judul Penelitian"])
    print("BERT Embeddings Shape:", bert_embeddings.shape)