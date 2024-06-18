from database_create import create_websites_db_if_not_exists
from crawler import Crawler
import asyncio

print("APP STARTING")

#Create keyspace and tables for websites database if they dont exist
create_websites_db_if_not_exists()

#Run the crawler
print("Starting crawler")
crawler = Crawler(["https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap#text", "https://developers.google.com/", "https://stackoverflow.com", "https://gemini.google.com/"])
asyncio.run(crawler.crawl())