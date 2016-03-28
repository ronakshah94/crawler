# Import all libraries needed for the scrape process
import urlparse
import urllib
from bs4 import BeautifulSoup


# Function to perform BFS traversal from the seed link
def crawler(seed,limit):
	# Queue of websites to visit
	links=[seed]
	# List of visited websites
	visited=[seed]
	# Ensuring that there are always links to traverse to
	while(len(links)>0):
		# Popping the top link in FIFO order
		url=links[0]
		links.pop(0)
		# Housekeeping requirement
		r=None
		# Trying to get the HTML at the URL
		try:
			r=urllib.urlopen(url).read()
		except:
			print (url+"- Didn't work")
			continue
		# Converting the HTML to an accesible DOM structure
		soup=BeautifulSoup(r)
		# Traversing all anchor tags to find outgoing links
		for tag in soup.findAll('a',href=True):
			hyperlink=tag['href']
			# Normalizing sublinks on the website
			if len(hyperlink)>0 and hyperlink[0]=='#':
				hyperlink="/"+hyperlink[1:]
			link=urlparse.urljoin(url,hyperlink)
			# Adding unvisited link to the list of links to visit
			if link not in visited:
				links.append(link)
		# Updating the list of visited links
		visited.append(url)
		# Ensuring that the crawl doesn't go on forever
		if len(visited)==limit:
			break
	# Returning list of all websites traversed to
	return visited

list_of_crawled=crawler("http://news.ycombinator.com",20)

for i in list_of_crawled:
	print(i)

