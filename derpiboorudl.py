import json
import urllib.request
import os
import os.path
import sys

destdir = ""
searched_tag = ""
maxpages = 30

def downloadallimages(images):
    for image in images:
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

if len(sys.argv) < 3:
    print("Usage: %s <destdir> <tagname> <maxpages>" % sys.argv[0])
    exit()
destdir = stringwithnoquotes(sys.argv[1])
searched_tag = stringwithnoquotes(sys.argv[2])
if len(sys.argv) > 3:
    maxpages = int(sys.argv[3])
for i in range(1, maxpages):
    url = "https://derpiboo.ru/search.json?q=%s&page=%d" % (searched_tag, i)
    print("Searching page %d" % i)
    response = urllib.request.urlopen(url)
    data = response.read().decode("utf-8")
    j = json.loads(data)
    images = j["search"]
    if images:
        downloadallimages(images)
    else:
        print("Received empty list, quitting.")
        exit()

if __name__ == "__main__":
    main()
