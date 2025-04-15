# Arxiv Scraping Project

## Deskripsi
Proyek ini melakukan **web scraping** untuk mengambil judul-judul penelitian dari **arXiv** yang berkaitan dengan topik "machine learning". Data yang diperoleh kemudian disimpan dalam format **CSV** untuk analisis lebih lanjut.

---

## Sumber Data
Data diambil dari halaman pencarian **arXiv** menggunakan **URL**:
```
https://arxiv.org/search/?query=machine+learning&searchtype=all&start=
```
Pada halaman ini, penelitian-penelitian terkait **machine learning** dapat ditemukan dan diambil menggunakan teknik **web scraping**.

---

## Struktur Direktori

```
MLOps/
│── api/                           # Service API
│   ├── Dockerfile
│   ├── api.py
│   ├── requirements.txt
│── eksplorasi/                    # Eksplorasi untuk lebih mengenali data
│   ├── analisis_statistik.py
│   ├── visualisasi_wordcloud.py
│   ├── tfidf_bert_embeddings.py
│   ├── preprocessing_pipeline.py
├── README.md                       # Dokumentasi proyek ini
├── judul_penelitian.csv            # Hasil scraping berisi daftar judul penelitian            
├── notebook.ipynb            
└── scrapping.py
```

---

## Tools yang Digunakan

- **Python**: Versi 3.x
- **Libraries**:
  - **requests**: Digunakan untuk mengirim permintaan HTTP dan mengakses halaman web.
  - **BeautifulSoup (bs4)**: Digunakan untuk parsing dan ekstraksi data dari halaman HTML.
  - **pandas**: Digunakan untuk menyimpan data yang diekstrak dalam format CSV.
  - **time**: Untuk memberikan jeda antara permintaan HTTP guna menghindari pemblokiran.

---

## Lisensi
Proyek ini dilisensikan di bawah **MIT License**.
