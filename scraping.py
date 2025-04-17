import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import json

# Base URL arXiv HTML
base_url = "https://arxiv.org/search/cs?query=machine+learning&searchtype=all&abstracts=show&order=-announced_date_first&size=50&start="

def scrape_titles():
    all_data = []

    # Loop dari halaman 1 sampai 15 (0 sampai 700 dengan step 50)
    for page in range(15):
        start = page * 50
        url = base_url + str(start)
        print(f"Scraping halaman {page + 1}: {url}")

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Gagal akses halaman {url}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("li", class_="arxiv-result")

        if not results:
            print("Tidak ada lagi hasil.")
            break

        for result in results:
            try:
                title = result.find("p", class_="title").text.strip()
                abstract = result.find("span", class_="abstract-full").text.strip().replace("▼ Less", "")
                authors = [a.text.strip() for a in result.find("p", class_="authors").find_all("a")]
                published_line = result.find("p", class_="is-size-7").text.strip()
                year = published_line.split(";")[0].split()[-1]

                # Placeholder fields
                doi = None
                journal_conference_name = None
                publisher = "arXiv"
                group_name = None

                all_data.append({
                    "title": title,
                    "abstract": abstract,
                    "authors": authors,
                    "journal_conference_name": journal_conference_name,
                    "publisher": publisher,
                    "year": int(year),
                    "doi": doi,
                    "group_name": group_name
                })
            except Exception as e:
                print(f"Error memproses satu hasil: {e}")
                continue

        time.sleep(2)

    print(f"Total data baru: {len(all_data)}")

    # Simpan hasil baru (hapus data lama)
    new_df = pd.DataFrame(all_data)

    # Simpan ke file baru (overwrite)
    csv_file = "judul_penelitian.csv"
    json_file = "judul_penelitian.json"
    new_df.to_csv(csv_file, index=False, encoding="utf-8")
    new_df.to_json(json_file, orient="records", indent=4, force_ascii=False)

    print(f"Scraping selesai, data disimpan ke {csv_file} dan {json_file}")
