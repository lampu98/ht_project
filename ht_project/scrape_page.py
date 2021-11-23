from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np
import time
import csv

path = "raw_data/index_url.csv"
df=pd.read_csv(path)


def scrape():
    with open('/Users/fenice/code/QZKZ3/ht_project/try.csv',
            'a',
            encoding='UTF8',
            newline='') as f:
        for i in range(1358):
            print(i)
            time.sleep(2)
            link = df.loc[i].url
            response = requests.get(link)
            html = response.text
            soup = BeautifulSoup(html, features="html.parser")

            take = soup.find("dd", {"class": "item-meta__value"}).text

            text = []
            for element in soup.find("div", class_="text-item-body no-select").find_all("p"):
                text.append(element.text)
            final_text=' '.join(text)

            try:
                for item in soup.find_all("div", class_= "item-title"):
                    name = item.find("h3", class_="item-title__title").text.split()[0]
                    narrative_year = item.find("h5", class_="item-title__meta").text.split()[0]
            except:
                name=np.nan
                narrative_year=np.nan

            try:
                countries = re.findall("\n..(.*)", take)[0]
            except:
                pass

            try:
                departure = re.findall("(.*).slavery location", countries)[0].strip()
            except:
                departure= np.nan

            try:
                arrival = re.findall("slavery location.*?(\w.*) .trafficked from",
                            countries)[0]
            except:
                arrival= np.nan

            inline_item_str= str(soup.find_all("li", {"class": "inline-meta__item"}))
            summ=len(re.findall("slavery location",inline_item_str))+len(re.findall("trafficked from",inline_item_str))

            inline_item = soup.find_all("li", {"class": "inline-meta__item"})

            if summ==0:
                theme = (inline_item[0].text).strip()
            elif summ==1:
                theme = (inline_item[1].text).strip()
            elif summ==2:
                theme = (inline_item[2].text).strip()
            elif summ==3:
                theme = (inline_item[3].text).strip()
            elif summ==4:
                theme = (inline_item[3].text).strip()
            else:
                theme = (inline_item[5].text).strip()

            try:
                maplocation = re.findall("mapLocation = .(.*).,",
                                        soup.find("script").text)[0]
                latitude = float(re.findall("(.*),", maplocation)[0])
                longitude = float(re.findall(",(.*)", maplocation)[0])
            except:
                latitude=np.nan
                longitude=np.nan

            try:
                date_slavery = re.findall("\d{4}-\d*", str(soup.find("section", class_="item-meta")))[0]
            except:
                date_slavery=np.nan

            dictionary = {
                "index":i,
                "text": final_text,
                "name": name,
                "year": narrative_year,
                "departure": departure,
                "arrival": arrival,
                "theme": theme,
                "latitude": latitude,
                "longitude": longitude,
                "date_slavery": date_slavery
            }

            fieldnames= [
                "index","text","name",
                "year", "departure", "arrival", "theme", "latitude", "longitude",
                "date_slavery"
            ]

            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(dictionary)

scrape()
