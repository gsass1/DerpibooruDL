# DerpibooruDL

Simple program to automise large downloading of images from Derpibooru.

## Prerequisites

Python 3.4

## Usage

derpiboorudl.py destination tags pages

Example:
> derpiboorudl.py ~/Pictures/lotsofpone "cute,derpy+hooves"

Note that specifying the pages is optional and is 30 by default (e.g. a lot)
You can also set your API key.
> export DERPIBOORUAPIKEY=yourkey

### Short file names

You can get short file names (only the image ID + extension) by appending the "-s" option.

## Todo

- Add more functionality
