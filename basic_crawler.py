import re
import requests
import urlparse
import urllib
from bs4 import BeautifulSoup

def crawler(seed,limit):
	links=[seed]
	visited=[seed]
	while(len(links)>0):
		url=links[0]
		links.pop(0)
		r=None
		try:
			r=urllib.urlopen(url).read()
		except:
			print (url+"- Didn't work")
			continue
		soup=BeautifulSoup(r)
		for tag in soup.findAll('a',href=True):
			hyperlink=tag['href']
			if len(hyperlink)>0 and hyperlink[0]=='#':
				hyperlink="/"+hyperlink[1:]
			link=urlparse.urljoin(url,hyperlink)
			if link not in visited:
				links.append(link)
		visited.append(url)
		if len(visited)==limit:
			break
	return visited

list_of_crawled=crawler("http://news.ycombinator.com",20)

for i in list_of_crawled:
	print(i)

