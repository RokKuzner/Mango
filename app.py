from database_create import create_websites_db_if_not_exists
from crawler import Crawler
import asyncio
from database import WebsitesDatabase

#Create keyspace and tables for websites database if they dont exist
create_websites_db_if_not_exists()

#Run the crawler
db = WebsitesDatabase()

crawler = Crawler(db.get_urls_to_crawl())
asyncio.run(crawler.crawl())