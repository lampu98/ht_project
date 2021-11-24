import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

response = requests.get("http://antislavery.ac.uk/items/show/121")
soup = BeautifulSoup(response.content, "html.parser")

testimonies = []
for item in soup.find_all("div", class_= "item-title"):
    name = item.find("h3", class_="item-title__title").text.split()[0]
    narrative_year = item.find("h5", class_="item-title__meta").text.split()[0]
    testimonies.append({'name': name, 'narrative_year': narrative_year})
text = []
for element in soup.find("div",
                         class_="text-item-body no-select").find_all("p"):
    text.append(element.text)
' '.join(text)
