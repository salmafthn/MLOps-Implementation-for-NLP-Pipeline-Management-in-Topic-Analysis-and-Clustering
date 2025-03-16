import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Gabungkan semua teks dalam dataset
text_corpus = " ".join(df["Judul Penelitian"])

# Generate WordCloud
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text_corpus)

# Tampilkan WordCloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.title("WordCloud dari Judul Penelitian")
plt.axis("off")
plt.show()