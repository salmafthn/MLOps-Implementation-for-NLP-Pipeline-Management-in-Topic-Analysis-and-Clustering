import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import json
from prometheus_client import start_http_server, Summary, Counter

# Metrics Prometheus
scraping_duration = Summary('scraping_duration_seconds', 'Time spent scraping a page')
scraped_pages = Counter('scraped_pages_total', 'Total pages scraped')
scraped_errors = Counter('scrapping_errors_total', 'Total scraping error')

# URL base pencarian arXiv
base_url = "https://arxiv.org/search/?query=text+mining&searchtype=all&source=header"

@scraping_duration.time()  # Ukur durasi fungsi scrape_titles
def scrape_titles():
    all_data = []

    for page in range(110):  # bisa diubah
        start = page * 50
        url = base_url + f"&start={start}"
        print(f"Scraping halaman {page + 1}: {url}")

        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Gagal akses halaman {url} (Status code: {response.status_code})")
                scraped_errors.inc()
                continue  # lanjut halaman berikutnya

            # Tambahkan ini jika berhasil
            scraped_pages.inc()

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
                        for less_elem in abstract_tag.find_all(string=lambda text: 'Less' in text):
                            less_elem.extract()
                        abstract = abstract_tag.get_text(strip=True)
                    else:
                        abstract = None

                    detail_link = result.find("p", class_="list-title").find("a")["href"]
                    detail_res = requests.get(detail_link)
                    detail_soup = BeautifulSoup(detail_res.text, "html.parser")

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

            time.sleep(2)  # jeda antar halaman
        except Exception as e:
            print(f"Error scraping halaman {url}: {e}")
            scraped_errors.inc()
            continue

    print(f"Total data baru: {len(all_data)}")

    # Simpan ke CSV dan JSON
    csv_file = "data/judul_penelitian.csv"
    json_file = "data/judul_penelitian.json"
    new_df = pd.DataFrame(all_data)

    if os.path.exists(csv_file):
        old_df = pd.read_csv(csv_file)
        combined_df = pd.concat([old_df, new_df], ignore_index=True)
    else:
        combined_df = new_df

    combined_df["title_lower"] = combined_df["title"].str.lower()
    combined_df.drop_duplicates(subset=["title_lower"], inplace=True)
    combined_df.drop(columns=["title_lower"], inplace=True)

    combined_df.to_csv(csv_file, index=False, encoding="utf-8")
    combined_df.to_json(json_file, orient="records", indent=4, force_ascii=False)

    print(f"Scraping selesai, data disimpan ke {csv_file} dan {json_file}")

if __name__ == "__main__":
    print("Menjalankan scraping dan memulai server metrik Prometheus di port 8000...")
    start_http_server(8000)  # Port Prometheus
    scrape_titles()
