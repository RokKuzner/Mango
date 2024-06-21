from database_create import create_websites_db_if_not_exists
from crawler import Crawler

#Create keyspace and tables for websites database if they dont exist
create_websites_db_if_not_exists()

#Run the crawler
crawler = Crawler()
crawler.crawl()