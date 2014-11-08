#!/usr/bin/env python3

import argparse
import logging
import json
import urllib.request
import os
import os.path
import sys

logger = None
destdir = ""
searched_tag = ""
maxpages = 30
shortfilenames = False

def setup_logger(log):
    log.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)

def downloadallimages(images):
    for image in images:
        id = str(image["id_number"])
        url = image["image"]
        url = "https:" + url
        filename = os.path.basename(url)
        filepath = os.path.join(destdir, filename)
        if not os.path.isfile(filepath):
            logger.info("Downloading %s" % url)
            urllib.request.urlretrieve(url, filepath)
            if shortfilenames:
                filetype = os.path.splitext(filepath)[1]
                os.rename(filepath, os.path.join(destdir, id + filetype))

def stringwithnoquotes(string):
    if string.startswith('"') and string.endswith('"'):
        string = string[1:-1]
    return string

logger = logging.getLogger("derpiboorudl")
setup_logger(logger)

# Read API key from env (will get overriden by --key option when given)
apikey = os.getenv("DERPIBOORUAPIKEY")

# Parse args
parser = argparse.ArgumentParser()
parser.add_argument("destdir", help="Location where downloaded images will be drop off")
parser.add_argument("query", help="The Derpibooru query you wish to execute")
parser.add_argument("--pages", help="The amount of pages you wish to download", type=int)
parser.add_argument("--shortfilenames", help="If you want only short file names (id.ext)", action="store_true")
parser.add_argument("--key", help="Specify the API key (normally present as env variable)")
args = parser.parse_args()

destdir = args.destdir 
searched_tag = args.query 

if args.pages:
    maxpages = args.pages

if args.shortfilenames:
    shortfilenames = True

apikey = args.key

if apikey is None:
    logger.info("No API key was set! (DERPIBOORUAPIKEY)")

for i in range(maxpages):
    url = "https://derpiboo.ru/search.json?q=%s&page=%d&key=%s" % (searched_tag, i, apikey)
    logger.info("Searching page %d" % i)
    response = urllib.request.urlopen(url)
    data = response.read().decode("utf-8")
    j = json.loads(data)
    images = j["search"]
    if images:
        downloadallimages(images)
    else:
        logger.info("Received empty list, quitting.")
        exit()
