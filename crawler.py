import requests
from bs4 import BeautifulSoup
from database import WebsitesDatabase
import translate
import keywordextractor
from urllib.parse import urlparse, urljoin
from datetime import datetime, timezone

def get_utc_timestamp():
  current_time_utc = datetime.now(timezone.utc)
  return current_time_utc.timestamp()

class Crawler():
  def __init__(self) -> None:
    self.database = WebsitesDatabase()
    self.recenty_crawled = {}

  def crawl(self):
    while True:
      urls_to_crawl = self.database.get_urls_to_crawl() #Get the urls to crawl from db
      if len(urls_to_crawl) == 0:
        return 1 #Quit if there aren't any urls to crawl

      url = urls_to_crawl[0]

      #Don't crawl this url if it was crawled in the last hour or it is a pdf
      if (url in self.recenty_crawled and get_utc_timestamp() - self.recenty_crawled[url] < 3600) or (url[-4:] == ".pdf"):
        self.database.remove_url_to_crawl(url)
        continue

      print(f"Crawling {url}")

      try:
        page_info = self.extract_page_info(url)
      except Exception as e:
        self.database.remove_url_to_crawl(url)
        continue

      self.database.insert_website(url, page_info["title"], page_info["keywords"])
      self.database.remove_url_to_crawl(url)
      self.recenty_crawled[url] = get_utc_timestamp()

  def extract_page_info(self, url):
    #Get the response and parse html
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Get page title and content
    title = soup.title.string if soup.title else ""
    user_visible_content = self.get_user_visible_content(soup)

    #Get page keywords
    keywords = set(keywordextractor.extract_keywords(title + " " + user_visible_content))

    #Get all links in page for further crawling
    discovered_links_on_this_site = set()
    for link in soup.find_all("a"):
      #If the link is valid add it to database to crawl
      link_url = link.get("href")
      parsed_url = urlparse(link_url)
      if parsed_url.scheme and parsed_url.netloc and link_url != url and link_url not in discovered_links_on_this_site:
        self.add_url_to_crawl(link_url)
        discovered_links_on_this_site.add(link_url)
      else:
        #Link isn't valid so try merging the link with the base url, example: merge "https://www.google.com/"(base url) and "/search"
        #Then you get "https://www.google.com/search" and check if this merged url is valid
        link_url = urljoin(url, link_url)
        parsed_url = urlparse(link_url)
        if parsed_url.scheme and parsed_url.netloc and link_url != url and link_url not in discovered_links_on_this_site:
          self.add_url_to_crawl(link_url)
          discovered_links_on_this_site.add(link_url)

    return {
      "url": url,
      "title": title,
      "content": user_visible_content,
      "keywords": keywords
    }

  def get_user_visible_content(self, soup:BeautifulSoup) -> str:
    #Get the text that is rendered to a user
    user_visible_content = soup.get_text(separator=" ")
    user_visible_content = " ".join(user_visible_content.replace("\n", " ").split()) #Clean up text

    #Check if the text contains ANY alpha chars
    contains_alpha = False
    for char in user_visible_content:
      if char.isalpha():
        contains_alpha = True
        exit

    #Translate text to english if contains ANY alpha chars
    if contains_alpha:
      language = translate.detect_lang(user_visible_content) #Get text language

      if language != "en": #Translate if the language isnt english
        translated_text = translate.translate(user_visible_content, language)

        if type(translated_text) == str: #Set the translated text to user_visible_content only if the trnslated text is a string and not an error message
          user_visible_content = translated_text
    
    return user_visible_content
  
  def add_url_to_crawl(self, url:str):
    self.database.add_url_to_crawl(self.clean_url(url))

  def clean_url(self, url:str):
    if "#" in url:
      url = url[:url.index("#")]

    if url[-1] == "/":
        url = url[:-1]