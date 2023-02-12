from newscatcher import Newscatcher, describe_url
from datetime import datetime
from feedsearch import search
import feedparser
import re
import csv
import json
import time

websites = [
    'ria.ru',
    'lenta.ru',
    'rg.ru',
    'vesti.ru',
    'www.mk.ru',
    'russian.rt.com',
    'tass.ru',
    'gazeta.ru',
    'news.mail.ru',
    'www.interfax.ru',
    'www.kommersant.ru',
    'smotrim.ru',
    'news.rambler.ru',
    '1prime.ru',
    'iz.ru'
]

supported = ""
notSupported = ""
count = 0
data = ['id', 'title', 'date', 'author', 'link', 'content', 'dateRead']
with open('data.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(data)
for website in list(set(websites)):
    try:
        articles = []
        try:
            nyt = Newscatcher(website = website)
            results = nyt.get_news()
            articles = results['articles']
        except:
            feeds = search(website)
            urls = [f.url for f in feeds]
            news_feed = feedparser.parse(urls[0])
            articles = news_feed["entries"]

        for article in articles[:10]:
           count+=1
           id = str(count)
           title = article["title"]
           date = article["published"]
           author = ""
           try:
               author = article["author"]
           except:
               author = ""
           link = article["link"]
           content = ""
           try:
               content = article["description"]
           except:
               try:
                   content = article["content"]
               except:
                   content = ""
           dateRead = str(datetime.now())
           to_clean = re.compile('<.*?>')
           no_newline = re.compile('\n')
           no_newrow = re.compile('&#\d*')

           data = [id, title, date, author, link, re.sub(no_newrow, '', (re.sub(no_newline, '', re.sub(to_clean, '', content)))), dateRead]
           with open('data.csv', 'a', newline='') as file:
               writer = csv.writer(file)
               writer.writerow(data)
        supported = supported + website + "\n"
    except:
        notSupported = notSupported + website + "\n"
print("Supported: \n")
print(supported)
print("Not supported: \n")
print(notSupported)