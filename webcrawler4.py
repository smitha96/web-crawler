from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import time

client=MongoClient('localhost:27017')
db=client.crawler

def extract_title(content):
    soup=BeautifulSoup(content, "lxml");
    tag=soup.find("title",text=True)
   
    if not tag:
        return None
    return tag.string.strip()

def extract_links(content):
    soup=BeautifulSoup(content,"lxml")
    links=set()
    for tag in soup.find_all("a",href=True):
        if tag['href'].startswith("http"):
            links.add(tag["href"])
    return links

def crawl(start_url):
    id=0
    t1=time.time()
    seen_urls=set([start_url])
    available_urls=set([start_url])
    while available_urls:
        url=available_urls.pop()
        try:
            content=requests.get(url,timeout=30).text
        except KeyboardInterrupt:
            t2=time.time()
            print("Number of pages crawled %d,time taken %f seconds"%(id,t2-t1))
            exit(0)
        title=extract_title(content)
        if title:
            id=id+1
            print(title)
            print(url)
            db.crawledpages.insert({'id':id,'title':title,'url':url})
            print '\n'
        for link in extract_links(content):
            if link not in seen_urls:
                seen_urls.add(link)
                available_urls.add(link)   

try:
    crawl("https://www.python.org/")
except KeyboardInterrupt:
    print()
    print("Bye!")
 



