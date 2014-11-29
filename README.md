# DerpibooruDL

Simple program to automise large downloading of images from Derpibooru.

## Prerequisites

* Python 2.7
* derpybooru
* requests (derpybooru needs requests)

## Usage

> ./derpiboorudl.py -d destdir -q query [options]


-d/--destdir: the destination where the images should be saved to


-q/--query: the Derpibooru search you want to query for


Options are: _-c/--count_ the specify the count of images you want to download, _-k/--key_ to set the API key (which is read in by the DERPIBOORUAPIKEY environment variable by default)