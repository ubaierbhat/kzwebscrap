# kzwebscrap
web scraping kashmiri language dictionary 

## Introduction

This repo is a data dump of Kashmiri language dictionary extracted from kashmirizabaan.com. The extracted data is saved in json format (under `data/json/`) to make it more open and human readable.
  
## Requirements

- python 3.x 

## Setup

```
$ pipenv --three
$ pipenv shell
$ pipenv install -e .
```

## Usage

To start fresh download and transform to json files
```
$ python DictScrapper.py -d -t
```