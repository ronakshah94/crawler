import re
import requests
import urlparse

def crawler(seed,limit):
	links=[]
	visited=dict()
	links.append(seed)
	visited[seed]=True
	while(not links):
		url=links[0]
		links.remove(links[0])
		r=requests.get(url)
		if r.status_code !=200:
			continue
		urls=re.findall('<a href="?\'?([^"\'>]*)', r.text)
		for i in urls:
			if i not in visited:
				visited[i]=True
				links.append(urlparse.urljoin(i))
		limit=limit-1
		if limit==0:
			print("Limit Exceeded")
			break
	return visited

list_of_links=crawler("http://www.clarku.edu/",15)

for key in list_of_links:
	print(key)



