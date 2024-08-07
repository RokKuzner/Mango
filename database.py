from cassandra.cluster import Cluster
import cassandra
import time

def start_cassandra_session(host, port, delay=5):
  while True:
    try:
      cluster = Cluster([host], port=port)
      session = cluster.connect()
      return session, cluster
    except Exception as e:
      time.sleep(delay)

class WebsitesDatabase():
  def __init__(self) -> None:
    self.session, self.cluster = start_cassandra_session('cassandra', 9042)
    self.session.set_keyspace('websites')

  def insert_website(self, url:str, title:str, keywords:set):
    #Insert/update the title and keywords for a website
    try:
      self.session.execute(self.session.prepare("INSERT INTO websites (url, title, keywords) VALUES (?, ?, ?)"), (url, title, keywords))
    except cassandra.AlreadyExists:
      self.session.execute(self.session.prepare("UPDATE websites SET title = ?, keywords = ? WHERE url = ?"), (title, keywords, url))

    #Delete all old keywords
    old_keywords = self.session.execute(self.session.prepare("SELECT keyword FROM keywords WHERE url = ? ALLOW FILTERING"), (url,))
    for column in old_keywords:
      self.session.execute(self.session.prepare("DELETE FROM keywords WHERE url = ? AND keyword = ?"), (url, column.keyword))
    
    #Insert the new keywords for the website
    for keyword in keywords:
      self.session.execute(self.session.prepare("INSERT INTO keywords (keyword, url) VALUES (?, ?)"), (keyword, url)) #Save the keyword and the url into the database

  def add_url_to_crawl(self, url:str):
    try:
      self.session.execute(self.session.prepare("INSERT INTO tocrawl (url) VALUES (?)"), (url,))
    except cassandra.AlreadyExists:
      pass #Do not add the url to the "tocrawl" table if the url is allready there

  def remove_url_to_crawl(self, url:str):
    self.session.execute(self.session.prepare("DELETE FROM tocrawl WHERE url = ?"), (url,))

  def get_urls_to_crawl(self):
    return [column.url for column in self.session.execute("SELECT * FROM tocrawl")]

  def get_website_urls_by_keyword(self, keyword:str):
    urls = []

    urls_cols = self.session.execute(self.session.prepare("SELECT url FROM keywords WHERE keyword=?"), (keyword,))
    for col in urls_cols:
      urls.append(col["url"])

    return urls

  def shutdown(self):
    self.session.shutdown()
    self.cluster.shutdown()