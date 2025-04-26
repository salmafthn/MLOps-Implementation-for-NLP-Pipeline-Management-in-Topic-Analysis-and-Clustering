from gensim.models.coherencemodel import CoherenceModel
from gensim.corpora.dictionary import Dictionary

def evaluate_coherence(topic_model, docs):
    """
    Fungsi untuk menghitung coherence score model topic modeling.
    Args:
        topic_model: BERTopic model yang sudah di-train.
        docs: List of strings (dokumen training).
    Returns:
        coherence_score: float
    """
    # Ambil semua topik dan kata-katanya
    topics = topic_model.get_topics()

    # Siapkan daftar kata tiap topik
    topic_words = []
    for topic_id in topics.keys():
        words = [word for word, _ in topics[topic_id]]
        topic_words.append(words)

    # Tokenisasi dokumen
    tokenized_docs = [doc.split() for doc in docs]

    # Bikin dictionary dari tokenized_docs
    dictionary = Dictionary(tokenized_docs)

    # Build Coherence Model
    coherence_model = CoherenceModel(
        topics=topic_words,
        texts=tokenized_docs,
        dictionary=dictionary,
        coherence='c_v'
    )

    coherence_score = coherence_model.get_coherence()
    return coherence_score
