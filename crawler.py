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
import sys
import subprocess
import indexer
from scraping import WebScraper

def go_index(page):
    try:
        scraper = WebScraper()
        if scraper.scrape(page):
            domain = indexer.get_domain(page)
            indexer.index_domain(domain)
            indexer.index_file(domain, domain, True)
            urls = scraper.get_link_urls()
            if indexer.has_crawable(urls):
                for url in urls:
                    title = url.encode(encoding="utf-8",errors="replace")
                    hashPath = "{0}.link".format(indexer.do_hash(title))
                    path = os.path.join(domain, hashPath)
                    if not os.path.exists(path) and url != scraper.page:
                        indexer.index_file(url, domain, True)
                        go_index(url)
        else:
            print("Can not scrape requested page {0}".format(page))
    except RuntimeError as exception:
            print("Runtime Error occurred")
            sys.exit()

if len(sys.argv) >= 2:
    go_index(sys.argv[1])
else:
    print("No address specified")
