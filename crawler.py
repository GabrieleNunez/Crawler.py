import os
import os.path
import errno
import re
import hashlib
import urllib.request
import urllib.parse
import urllib.error
import time
import sys
from bs4 import BeautifulSoup

class WebScraper:
    def scrape(self):
        try:
            headers = {"User-Agent": "Crawler.py Bot"}
            req = urllib.request.Request(self.page,headers = headers)
            self.soup = BeautifulSoup(urllib.request.urlopen(req))
            return True
        except ValueError as exception:
            return False
        except urllib.error.URLError as exception:
            print("Bad Url")
            return False
        except urllib.error.HTTPError as exception:
            print("Http Error occurred")
            return False
	def set_page(page):
		self.page = page
    def get_link_urls(self):
        urls = []
        index = 0
        for link in self.soup.find_all("a"):
            href = link.get("href")
            if valid_string(href):
                full_url = urllib.parse.urlparse(href,scheme="http")
                if full_url != None:
                    netloc = full_url.netloc
                    if netloc == None or len(netloc) == 0:
                        netloc = "{0}".format(urllib.parse.urlparse(self.page).netloc)
                    url = r"{0}://{1}{2}".format(full_url.scheme,netloc,full_url.path)
                    if url != None and len(url) > 7:
                        urls.insert(index,url)
                        index += 1
        return urls

def do_hash(hashItem):
    content = "{0}".format(hashItem)
    hasher = hashlib.sha256(content.encode("utf-8","ignore"))
    return  hasher.hexdigest()
def make_dir(path):
    if len(path) == 0:
        return False
    try:
        if os.path.exists(path):
            return False
        else:
            os.makedirs(path,exist_ok=True)
            return True
    except OSError as exception:
        print("Could not makedir: errno: {0}".format(exception.errno))
        return False
def make_file(content,dir,isLink):
    if content != None and len(content) > 0:
        try:
            extension = ".img"
            if isLink:
                extension = ".link"
            hashPath = "{0}.{1}".format(do_hash(content),extension)
            path = os.path.join(dir,hashPath)
            if os.path.exists(path):
                return False
            else:
                f = open(path,"w")
                f.write(content)
                f.close()
                return True
        except OSError as exception:
            return False
    else:
        return False
def valid_string(string):
    return string != None and len(string) > 8
def get_domain(url):
    if valid_string(url):
        r  = urllib.parse.urlparse(url)
        domain = "{0}".format(r.netloc)
        return domain
    else:
        return ""
def has_crawable(urls):
    return len(urls) > 0
def index_file(content,dir,isLink):
    if make_file(content,dir,isLink):
        print("Index created for {0}".format(content))
def index_domain(domain):
    if valid_string(domain) and make_dir(domain):
        print("Directory made for {0}".format(domain))
def go_index(page,scraper,tracker):
    print("Want to index {0}".format(page))
    scraper.set_page(page)
    if scraper.scrape():
        domain = get_domain(page)
        index_domain(domain)
        index_file(domain,domain,True)
        urls = scraper.get_link_urls()
        if has_crawable(urls):
            for url in urls:
                domain = get_domain(url)
                index_domain(domain)
                index_file(url,domain,True)
                if url != scraper.page and url not in tracker:
                    tracker.insert(len(tracker)-1,url)
                    go_index(url,scraper,tracker)
    else:
        print("Can not scrape requested page {0}".format(page))
tracker = []
Scraper scraper = WebScraper()
if len(sys.argv) >= 2:
    go_index(sys.argv[1],scraper,tracker)
else:
    print("No address specified")