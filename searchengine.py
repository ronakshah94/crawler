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
		cur=self.con.execute("select rowid from %s where %s='%s'" %(table, field, value))
		res=cur.fetchone()
		if(res==None):
			cur=self.con.execute("insert into %s (%s) values ('%s')" % (table, field, value))
			return cur.lastrowid
		else:
			return res[0]

	# Index a page
	def add_to_index(self, url, soup):
		if self.is_indexed(url): 
			return 
		print('Indexing ',url)

		# Get individual words
		text=self.get_text_only(soup)
		words=self.separate_words(text)

		# Get the URL id
		urlid=self.get_entry_id('urllist','url',url)

		# Link each word to this url
		for i in range(len(words)):
			word=words[i]
			if(word in ignored):
				continue
			wordid=self.get_entry_id('wordlist','word',word)
			self.con.execute("insert into wordlocation(urlid,wordid,location) values (%d,%d,%d)" %(urlid,wordid,i))

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
		splitter=re.compile('\\W')
		return [s.lower() for s in splitter.split(text) if s!='']

	# Check if url is already indexed
	def is_indexed(self, url):
		u=self.con.execute("select rowid from urllist where url='%s'" %url).fetchone()
		if(u!=None):
			v=self.con.execute('select * from wordlocation where urlid=%d' %u[0]).fetchone()
			if(v!=None):
				return True
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
