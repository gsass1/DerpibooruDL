#!/usr/bin/env python2.7

from derpibooru import Search
from requests import get, codes
from hashlib import sha512

import argparse
import copy
import logging
import os
import os.path
import sys
import threading
import time

logger = None

def sha512_hash(f):
    h = sha512()

    h.update(f)
    return h.hexdigest()

def download_file(url):
    r = get(url)

    if r.status_code == codes.ok:
        return r.content

def setup_logger(log):
    log.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)

def download_images(search, destdir, verification, logger):
    for image in search:
        filename = os.path.basename(image.full)
        path = os.path.join(destdir, filename)
        if os.path.isfile(path):
            continue
        logger.info("Downloading image %d" % image.id_number)
        download = download_file(image.full)
        if verification:
            if image.sha512_hash == sha512_hash(download):
                with open(path, "wb") as f:
                    f.write(download)
            else:
                logger.error("sha512 hashes for {0} don't match up".format(image.id_number))
        else:
            with open(path, "wb") as f:
                f.write(download)

# Split a sequence into num chunks
def chunks(seq, num):
  avg = len(seq) / float(num)
  last = 0.0

  while last < len(seq):
    yield seq[int(last):int(last + avg)]
    last += avg

def main():
    logger = logging.getLogger("derpiboorudl")
    setup_logger(logger)

    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("destdir", help="Location where downloaded images will be dropped off")
    parser.add_argument("-q", "--query", default="", help="The Derpibooru query you wish to execute")
    parser.add_argument("-c", "--count", default=100, help="The count of images you wish to download", type=int)
    parser.add_argument("-k", "--key", default=None, help="Specify the API key (normally present as env variable)")
    parser.add_argument("-nv", "--noverification", action='store_false', default=True, help="Disable image SHA512 verification")
    parser.add_argument("-t", "--threads", default=1, help="Amount of threads to create", type=int)
    args = parser.parse_args()

    destdir, query, maximages, verification, threadcount = args.destdir, args.query, args.count, args.noverification, args.threads
 
    # Read API key from --key if present or else read from env
    apikey = args.key if args.key else os.getenv("DERPIBOORUAPIKEY")

    if not apikey:
        logger.warning("No API key was set! (DERPIBOORUAPIKEY)")

    search = Search().key(apikey).query(query).limit(maximages)

    if not os.path.isdir(destdir):
        os.mkdir(destdir)

    if threadcount > 1:
        logger.info("Using %d threads" % threadcount)

    # Copy the search object to a valid list
    images = []
    for image in search:
        images.append(copy.deepcopy(image))

    # Create threads
    threads = []
    for c in chunks(images, threadcount):
        t = threading.Thread(target = download_images, args = (c, destdir, verification, logger))
        threads.append(t)
        t.daemon = True
        t.start()

    # This prevents the threads from hanging when pressing CTRL+C
    while threading.active_count() - 1 > 0:
        time.sleep(0.1)

    # Make sure threads are stopped
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()

