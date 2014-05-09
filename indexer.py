import os
import os.path
import hashlib
import urllib.request
import urllib.parse
import urllib.error

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
        print("Index created for {0}...".format(content[:30]))
def index_domain(domain):
    if valid_string(domain) and make_dir(domain):
        print("Directory made for {0}...".format(domain[:30]))