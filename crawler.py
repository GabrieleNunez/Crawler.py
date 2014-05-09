"""
 Author: Gabriele M. Nunez (http://thecoconutcoder.com)
 crawler.py is a python script that will automatically crawl desired web pages
 It cannot scrape or crawl javascript content. 
 It also tries it's little scripting best to reform a url
"""
import os
import os.path
import hashlib
import urllib.request
import urllib.parse
import urllib.error
import time
import sys
from Scraping import WebScraper

def do_hash(hashItem):
    return  hashlib.sha256("{0}".format(hashItem).encode(encoding="utf-8", errors="replace")).hexdigest()
def make_dir(path):
    if len(path) == 0:
        return False
    try:
        if os.path.exists(path):
            return False
        else:
            os.makedirs(path, exist_ok=True)
            return True
    except OSError as exception:
        print("Could not make_dir: errno: {0}".format(exception.errno))
        return False
def make_file(content, directory, isLink):
    if content != None and len(content) > 0:
        try:
            extension = "img"
            if isLink:
                extension = "link"
            title = content.encode(encoding="utf-8",errors="replace")
            hashPath = "{0}.{1}".format(do_hash(title), extension)
            path = os.path.join(directory, hashPath)
            if os.path.exists(path):
                return False
            else:
                f = open(path, "w")
                f.write(content)
                f.close()
                return True
        except OSError as exception:
            print("Could not make_file: errno: {0}".format(exception.errno))
            return False
    else:
        return False
def valid_string(string):
    return string != None and len(string) > 8
def get_domain(url):
    if valid_string(url):
        r = urllib.parse.urlparse(url)
        domain = "{0}".format(r.netloc)
        return domain
    else:
        return ""
def has_crawable(urls):
    return len(urls) > 0
def index_file(content, dir, isLink):
    if make_file(content, dir, isLink):
        print("Index created for {0}".format(content))
def index_domain(domain):
    if valid_string(domain) and make_dir(domain):
        print("Directory made for {0}".format(domain))
def go_index(page):
    scraper = WebScraper()
    scraper.set_page(page)
    if scraper.scrape():
        domain = get_domain(page)
        index_domain(domain)
        index_file(domain, domain, True)
        urls = scraper.get_link_urls()
        if has_crawable(urls):
            for url in urls:
                title = url.encode(encoding="utf-8",errors="replace")
                hashPath = "{0}.link".format(do_hash(title))
                path = os.path.join(domain, hashPath)
                if not os.path.exists(path) and url != scraper.page:
                    index_file(url, domain, True)
                    go_index(url)
    else:
        print("Can not scrape requested page {0}".format(page))
if len(sys.argv) >= 2:
    go_index(sys.argv[1])
else:
    print("No address specified")
