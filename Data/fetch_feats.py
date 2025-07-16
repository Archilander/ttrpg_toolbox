import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://aonprd.com/Feats.aspx"
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table", {"id": "MainContent_GridView6"})
headers = [th.get_text(strip=True) for th in table.find_all("th")]

rows = []
for tr in table.find_all("tr")[1:]: 
    cells = [td.get_text(strip=True) for td in tr.find_all("td")]
    rows.append(cells)

df = pd.DataFrame(rows, columns=headers)
df.to_csv("feats_full.csv", index=False, encoding="utf-8")

print(f"Saved {len(df)} feats to feats_full.csv")
