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

  def shutdown(self):
    self.session.shutdown()
    self.cluster.shutdown()