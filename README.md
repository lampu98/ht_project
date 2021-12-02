# NLP for Human Trafficking Mapping and Disruption

You can view our presentation here --> https://docs.google.com/presentation/d/1WWLiV0iE-advk9ZEAcDBrD0R9LocBgOTsdivnpf_Hgw/edit#slide=id.gcb9a0b074_1_0

You can view the website here --> https://share.streamlit.io/lampu98/ht_project/app.py

## Project aims

1. Enrich the global picture

2. Aid data interpretation

3. Encourage data sharing

## Description
By using NLP to extract key intelligence from survivor testimonies, and by combining this with existing datasets on human trafficking, this project aims to show that data science can:
1. Enrich the currently sparse global picture of human trafficking by allowing the collection of data that would be too cumbersome/costly to collect manually
2. Aid data interpretation, finding patterns that would perhaps be overlooked if assessed by humans alone
3. Encourage more organisations to share their data, even if it is unstructured, by showing the richness of information that can be obtained from each survivor story, and highlighting the value of this information to disruption efforts


## Data
Two sources of Data:
1. Nottingham University Rights Lab: 1,300+ testimonies from survivors of human trafficking
2. Counter Trafficking Data Collaborative (CTDC) 90,000+ anonymised case records




## Description of files and of our process
1. We did web scraping to grab the data - inside ht_project folder you can see two important files --> index_urls.py where we took every url of the pages and scrape_page.py where we grap the data that we want from every url
2. The main file is app.py where is stored the streamlit website --> inside the website you can see multiple interactive graphs, a prediction made with RandomForestClassifier and at the end some n-grams 

