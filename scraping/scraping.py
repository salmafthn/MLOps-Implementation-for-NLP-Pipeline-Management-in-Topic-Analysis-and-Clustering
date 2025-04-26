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
    for page in range(10):
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
                authors = [a.text.strip() for a in result.find("p", class_="authors").find_all("a")]
                published_line = result.find("p", class_="is-size-7").text.strip()
                year = published_line.split(";")[0].split()[-1]

                # Abstrak
                abstract_tag = result.find("span", class_="abstract-full")
                if abstract_tag:
                    # Hilangkan semua tag <a> atau elemen yang mengandung 'Less'
                    for less_elem in abstract_tag.find_all(string=lambda text: 'Less' in text):
                        less_elem.extract()

                    abstract = abstract_tag.get_text(strip=True)
                else:
                    abstract = None

                # Ambil link ke halaman detail
                detail_link = result.find("p", class_="list-title").find("a")["href"]
                detail_res = requests.get(detail_link)
                detail_soup = BeautifulSoup(detail_res.text, "html.parser")

                # Ekstrak journal & doi
                journal_tag = detail_soup.find("td", class_="tablecell jref")
                journal_conference_name = journal_tag.text.strip() if journal_tag else None
                doi_tag = detail_soup.find("a", href=lambda href: href and "doi.org" in href)
                doi = doi_tag.text.strip() if doi_tag else None

                all_data.append({
                    "title": title,
                    "abstract": abstract,
                    "authors": authors,
                    "journal_conference_name": journal_conference_name,
                    "publisher": "arXiv",
                    "year": int(year),
                    "doi": doi,
                    "group_name": "Anomali"
                })
            except Exception as e:
                print(f"Error memproses satu hasil: {e}")
                continue

        time.sleep(2)

    print(f"Total data baru: {len(all_data)}")

    # Simpan atau gabungkan ke CSV dan JSON
    csv_file = "judul_penelitian.csv"
    json_file = "judul_penelitian.json"
    new_df = pd.DataFrame(all_data)

    # Gabung dengan data lama jika ada
    if os.path.exists(csv_file):
        old_df = pd.read_csv(csv_file)
        combined_df = pd.concat([old_df, new_df], ignore_index=True)
    else:
        combined_df = new_df

    # Hapus duplikat berdasarkan title (case-insensitive)
    combined_df["title_lower"] = combined_df["title"].str.lower()
    combined_df.drop_duplicates(subset=["title_lower"], inplace=True)
    combined_df.drop(columns=["title_lower"], inplace=True)

    # Simpan ke CSV dan JSON
    combined_df.to_csv(csv_file, index=False, encoding="utf-8")
    combined_df.to_json(json_file, orient="records", indent=4, force_ascii=False)

    print(f"Scraping selesai, data disimpan ke {csv_file} dan {json_file}")