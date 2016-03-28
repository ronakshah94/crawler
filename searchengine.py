import urllib2
from BeautifulSoup import *
from urlparse import urljoin
from sqlite3 import dbapi2 as sqlite

# Create a list of words to ignore
ignored=set(['the','of','to','and','a','in','is','it'])
class crawler:
	# Initialize database
	def __init__(self, db):
		self.con=sqlite.connect(db)

	def __del__(self):
		self.con.close()

	def dbcommit(self):
		self.con.commit()


	# Add to database (with de-duping)
	def get_entry_id(self, table, field, value, createnew=True):
		return None

	# Index a page
	def add_to_index(self, url, soup):
		print ('Indexing ',url)

	# Extract text from HTML page
	def get_text_only(self, soup):
		v=soup.string
		if(v==None):
			c=soup.contents
			resulttext=''
			for t in c:
				subtext=self.get_text_only(t)
				resulttext+=subtext+"\n"
			return resulttext
		else:
			return v.strip()

	# Separate the words by any non-whitespace character
	def separate_words(self, text):
		return None

	# Check if url is already indexed
	def is_indexed(self, url):
		return False

	# Add link between pages
	def add_link_ref(self, urlFrom, urlTo, linkText):
		pass

	# Perform BFS to crawl pages
	def crawl(self, pages, depth=2):
		for i in range(depth):
			newpage=set()
			for page in pages:
				try:
					c=urllib2.urlopen(page)
				except Exception, e:
					print("Could not open ",page)
					continue
				soup=BeautifulSoup(c.read())
				self.add_to_index(page,soup)
				links=soup('a')
				for link in links:
					if('href' in dict(link.attrs)):
						url=urljoin(page,link['href'])
						if(url.find("'")!= -1):
							continue
						url=url.split("#")[0] # remove location portion
						if(url[0:4]=='http' and not self.is_indexed(url)):
							newpage.add(url)
						linkText=self.get_text_only(link)
						self.add_link_ref(page,url,linkText)

				self.dbcommit()
				pages=newpage


	# Create db tables
	def create_index_tables(self):
		self.con.execute('create table urllist(url)')
		self.con.execute('create table wordlist(word)')
		self.con.execute('create table wordlocation(urlid,wordid,location)')
		self.con.execute('create table link(fromid integer,toid integer)')
		self.con.execute('create table linkwords(wordid,linkid)')
		self.con.execute('create index wordix on wordlist(word)')
		self.con.execute('create index urlidx on urllist(url)')
		self.con.execute('create index wordurlidx on wordlocation(wordid)')
		self.con.execute('create index urltoidx on link(toid)')
		self.con.execute('create index urlfromidx on link(fromid)')
		self.dbcommit()
