import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Base URL untuk scraping judul dari arXiv
base_url = "https://arxiv.org/search/?query=machine+learning&searchtype=all&abstracts=show&order=-announced_date_first&size=50&start="

def scrape_titles():
    all_titles = []
    page = 0

    while True:
        start = page * 50
        url = base_url + str(start)
        print(f"Scraping halaman {page + 1}: {url}")

        response = requests.get(url)
        if response.status_code != 200:
            soup = BeautifulSoup(response.text, "html.parser")
            titles = soup.find_all("p", class_="title is-5 mathjax")

            if not titles:
                break  # Berhenti jika tidak ada lagi judul yang ditemukan

            for title in titles:
                all_titles.append(title.text.strip())

            page += 1  # Tambah halaman untuk iterasi berikutnya
            time.sleep(2)  # Hindari terlalu banyak request dalam waktu singkat
        else:
            print(f"Gagal mengakses halaman {page + 1}, Status Code: {response.status_code}")
            break

    # Buat DataFrame baru dari hasil scraping
    new_data = pd.DataFrame(all_titles, columns=["Judul Penelitian"])

    # Cek apakah file CSV sudah ada
    csv_file = "judul_penelitian.csv"
    if os.path.exists(csv_file):
        existing_data = pd.read_csv(csv_file)

        # Gabungkan data lama dengan data baru dan hapus duplikasi
        combined_data = pd.concat([existing_data, new_data]).drop_duplicates().reset_index(drop=True)

        # Simpan ke CSV tanpa menimpa seluruh data sebelumnya
        combined_data.to_csv(csv_file, index=False, encoding="utf-8")
    else:
        # Jika file belum ada, buat baru
        new_data.to_csv(csv_file, index=False, encoding="utf-8")

    print("Scraping selesai, hasil disimpan ke judul_penelitian.csv")