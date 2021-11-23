from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

path = "raw_data/index_url.csv"
df=pd.read_csv(path)

df_scrape = pd.DataFrame(index=["text", "departure", "arrival", "theme"])


def scrape():
    get_features=list()
    for i in range(2):
        link = df.loc[i].url
        response = requests.get(link)
        html = response.text
        soup = BeautifulSoup(html, features="html.parser")
        p = soup.find("div", {"class": "text-item-body no-select"}).find_all("p")
        list_principal_text = ",".join([i.text for i in p if i.text != "\xa0"])
        take = soup.find("dd", {"class": "item-meta__value"}).text
        countries = re.findall("\n..(.*)", take)[0]
        departure = re.findall("(.*).slavery location", countries)[0].strip()
        arrival = re.findall("slavery location.*?(\w.*) .trafficked from",
                        countries)[0]
        typee = soup.find_all("a", {"class": "no-underline"})
        theme = typee[2].text
        return [take, departure, arrival, theme]


scrape_page = scrape()



df.to_csv("page_scraping.csv")
