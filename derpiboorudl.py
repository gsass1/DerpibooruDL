#!/usr/bin/env python

from derpibooru import Search

import argparse
import logging
import urllib
import os
import os.path
import sys

logger = None
destdir = ""
query = ""
maximages = 100

def setup_logger(log):
    log.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)

logger = logging.getLogger("derpiboorudl")
setup_logger(logger)

# Read API key from env (will get overriden by --key option when given)
apikey = os.getenv("DERPIBOORUAPIKEY")

# Parse args
parser = argparse.ArgumentParser()
parser.add_argument("destdir", help="Location where downloaded images will be dropped off")
parser.add_argument("query", help="The Derpibooru query you wish to execute")
parser.add_argument("--count", help="The count of images you wish to download", type=int)
parser.add_argument("--key", help="Specify the API key (normally present as env variable)")
args = parser.parse_args()

destdir = args.destdir 
query = args.query 

if args.count:
    maximages = args.count

if args.key:
    apikey = args.key

if apikey is None:
    logger.info("No API key was set! (DERPIBOORUAPIKEY)")

for image in Search().key(apikey).query(query).limit(maximages):
    filename = os.path.basename(image.full)
    path = os.path.join(destdir, filename)
    if not os.path.isfile(path):
        logger.info("Now downloading image with id {0}".format(image.id_number))
        urllib.urlretrieve(image.full, path)