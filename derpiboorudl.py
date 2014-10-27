import json
import urllib.request
import os
import os.path
import sys

destdir = ""
searched_tag = ""
maxpages = 30
shortfilenames = False

def downloadallimages(images):
    for image in images:
        id = str(image["id_number"])
        url = image["image"]
        url = "https:" + url
        filename = os.path.basename(url)
        filepath = os.path.join(destdir, filename)
        print(filepath)
        if not os.path.isfile(filepath):
            print("Downloading %s" % url)
            urllib.request.urlretrieve(url, filepath)
            if shortfilenames:
                filetype = os.path.splitext(filepath)[1]
                os.rename(filepath, os.path.join(destdir, id + filetype))

def stringwithnoquotes(string):
    if string.startswith('"') and string.endswith('"'):
        string = string[1:-1]
    return string

apikey = os.getenv("DERPIBOORUAPIKEY")
if apikey is None:
    print("No API key was set! (DERPIBOORUAPIKEY)")
    apikey = ""

if len(sys.argv) < 3:
    print("Usage: %s <destdir> <tagname> <maxpages>" % sys.argv[0])
    exit()

destdir = stringwithnoquotes(sys.argv[1])

# Remove last character if its a slash
destdir = destdir.rstrip("/")
searched_tag = stringwithnoquotes(sys.argv[2])

if len(sys.argv) > 3:
    maxpages = int(sys.argv[3])

if len(sys.argv) > 4:
    for arg in sys.argv[4:]:
        if arg == "-s" or arg == "--shortnames":
            shortfilenames = True

for i in range(1, maxpages):
    url = "https://derpiboo.ru/search.json?q=%s&page=%d&key=%s" % (searched_tag, i, apikey)
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
