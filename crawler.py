"""
Author: Gabriele M. Nunez (http://thecoconutcoder.com)
crawler.py is a python script that will automatically crawl desired web pages
It cannot scrape or crawl javascript content.
It also tries it's little scripting best to reform a url
Keep in mind this is a very memory intensive script
The more RAM the better
Requirements: BeautifulSoup
"""
import os
import os.path
import sys
import indexer
from scraping import WebScraper

def go_index(page):
    """
    go_index(...) recursive function that will scrape web pages
    for every url it finds it will go in and call itself to continue
    caution this is a big memory hog and IT WILL fail eventually
    """
    try:
        scraper = WebScraper()
        if scraper.scrape(page):
            domain = indexer.get_domain(page)
            indexer.index_domain(domain)
            indexer.index_file(domain, domain, True)
            urls = scraper.get_link_urls()
            if indexer.has_crawable(urls):
                for url in urls:
                    title = url.encode(encoding="utf-8", errors="replace")
                    hash_path = "{0}.link".format(indexer.do_hash(title))
                    path = os.path.join(domain, hash_path)
                    if not os.path.exists(path) and url != scraper.page:
                        indexer.index_file(url, domain, True)
                        go_index(url)
        else:
            print("Can not scrape requested page {0}".format(page))
    except RuntimeError:
        # Figure out a way to respawn in another thread
        print("Runtime Error occurred. Killing Script")
        sys.exit()

if len(sys.argv) >= 2:
    go_index(sys.argv[1])
else:
    print("No address specified")
