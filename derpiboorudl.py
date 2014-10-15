import json
import urllib.request
import os
import os.path
import sys
from pprint import pprint

destdir = ""
searched_tag = ""
maxpages = 30

def downloadallimages(images):
    global destdir
    global searched_tag
    for image in images:
        # Download ze file
        url = image["image"]
        url = "https:" + url
        filename = os.path.basename(url)
        filepath = destdir + "/" + filename
        if not os.path.isfile(filepath):
            print("Downloading %s" % url)
            urllib.request.urlretrieve(url, filepath)
            
def stringwithnoquotes(string):
    if string.startswith('"') and string.endswith('"'):
        string = string[1:-1]
    return string

def main():
    global destdir
    global searched_tag
    if len(sys.argv) != 4:
        print("Usage: %s <destdir> <tagname> <maxpages>" % sys.argv[0])
        return
    destdir = stringwithnoquotes(sys.argv[1])
    searched_tag = stringwithnoquotes(sys.argv[2])
    maxpages = int(sys.argv[3])
    for i in range(1, maxpages):
        url = "https://derpiboo.ru/search.json?q=%s&page=%d" % (searched_tag, i)
        print(url)
        response = urllib.request.urlopen(url)
        data = response.read().decode("utf-8")
        j = json.loads(data)
        images = j["search"]
        downloadallimages(images)

if __name__ == "__main__":
    main()