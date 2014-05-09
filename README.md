crawler.py  
==========  

*crawler.py* is a *python 3.4* script  that will very simply crawl the web for you 
It scrapes the page for any anchor elements and goes from there.

This script is still *_in_development_* and *_should_* not be used yet.

## Requirements
* *BeautifulSoup 4.3* to install do the following
> pip install beautifulsoup4
* *Python 3.4*
## TODO
* Make it more advanced.
    * Scan document for key words
* Document better (Edit: Getting there)
* ~~Refactor out to separate modules for code clarity~~

## Known Bugs
* Actually visits page, meaning if its get a link to a file it will try to scan the file
* Recursion limit is reached easily
     * Solution might be to once it reaches limit to simply kill the script and let the system reclaim the memory
	 * Then start the script back up where it left off
* RAM hog