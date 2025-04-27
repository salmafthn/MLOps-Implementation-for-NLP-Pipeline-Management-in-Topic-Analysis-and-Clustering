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
    topics = topic_model.get_topics()

    topic_words = []
    for topic_id in topics.keys():
        words = [word for word, _ in topics[topic_id]]
        topic_words.append(words)

    tokenized_docs = [doc.split() for doc in docs]

    dictionary = Dictionary(tokenized_docs)

    coherence_model = CoherenceModel(
        topics=topic_words,
        texts=tokenized_docs,
        dictionary=dictionary,
        coherence='c_v'
    )

    coherence_score = coherence_model.get_coherence()
    return coherence_score
