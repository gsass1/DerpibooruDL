# DerpibooruDL

Simple program to automise large downloading of images from Derpibooru.

## Prerequisites

* Python 2.7
* derpybooru
* requests (derpybooru needs requests)

## Usage

> ./derpiboorudl.py destdir query [options] 


destdir: the destination where the images should be saved to


query: the Derpibooru search you want to query for


Options are: _--count_ the specify the count of images you want to download, _--key_ to set the API key (which is read in by the DERPIBOORUAPIKEY environment variable by default)