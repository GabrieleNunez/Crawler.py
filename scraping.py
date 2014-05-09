"""
Author: Gabriele M. Nunez (http://thecoconutcoder.com)
scraping.py is a module that is used by crawler.py
It encapsulates anything that we need to scrape the page effectively
Requirements: BeautifulSoup
"""
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
class WebScraper:
    def scrape(self,page):
        try:
            self.page = page
            head = {"User-Agent": "Crawler.py Bot"}
            req = urllib.request.Request(self.page, headers=head)
            self.soup = BeautifulSoup(urllib.request.urlopen(req))
            return True
        except ValueError as exception:
            print("Scraped fail. Value Error")
            return False
        except urllib.error.URLError as exception:
            print("Scraped fail. URL Error: {0}".format(exception.errno))
            return False
    def get_link_urls(self):
        urls = []
        index = 0
        for link in self.soup.find_all("a"):
            href = link.get("href")
            if href != None and len(href) > 7:
                full_url = urllib.parse.urlparse(href, scheme="http")
                if full_url != None:
                    netloc = full_url.netloc
                    if netloc == None or len(netloc) == 0:
                        netloc = "{0}".format(urllib.parse.urlparse(self.page).netloc)
                    url = r"{0}://{1}{2}".format(full_url.scheme, netloc, full_url.path)
                    if url != None and len(url) > 7:
                        urls.insert(index, url)
                        index += 1
        return urls
