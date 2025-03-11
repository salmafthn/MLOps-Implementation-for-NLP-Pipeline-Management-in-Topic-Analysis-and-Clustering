import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://arxiv.org/search/?query=machine+learning&searchtype=all&start="
all_titles = []
page = 0

while True:
    start = page * 50
    url = base_url + str(start)
    print(f"Scraping halaman {page + 1}: {url}")

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        titles = soup.find_all("p", class_="title")

        if not titles:
            break

        for title in titles:
            all_titles.append(title.text.strip())

        page += 1
        time.sleep(2)
    else:
        print(f"Gagal mengakses halaman {page + 1}, Status Code: {response.status_code}")
        break

df = pd.DataFrame(all_titles, columns=["Judul Penelitian"])
df.to_csv("MLOps/judul_penelitian.csv", index=False, encoding="utf-8")

print("Scraping selesai! Data disimpan dalam 'MLOps/judul_penelitian.csv'.")
