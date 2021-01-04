import json
from time import sleep
from Transliterator import transliterate_to_kashmiri
import re

import requests
from bs4 import BeautifulSoup

path_raw = './data/hassan/raw/'
path_json = './data/hassan/json/'
url = "https://dsalsrv04.uchicago.edu/cgi-bin/app/hassan_query.py"


def query(key):
    payload = f'qs={key}%&searchhws=yes'
    headers = {
        'Connection': "keep-alive",
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept-Language': "en,et;q=0.9,ur;q=0.8",
    }
    page = requests.request("POST", url, data=payload, headers=headers)
    page.encoding = 'utf-8'

    # cleanup
    page_text = page.text

    soup = BeautifulSoup(page_text, 'lxml')
    page_text = soup.prettify()

    filename = get_raw_filename(key)
    file = open(filename, 'w', encoding='utf-16')
    file.write(page_text)
    file.close()


def load(key):
    filename = get_raw_filename(key)
    print(filename)
    file = open(filename, 'r', encoding='utf-16')
    page = file.read()
    file.close()
    return page


def get_raw_filename(key):
    filename = f'{path_raw}{key}.html'
    return filename


def get_json_filename(key):
    filename = f'{path_json}{key}.json'
    return filename


def export_to_json(key, data):
    with open(get_json_filename(key), 'w', encoding='utf-16') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)
        fp.close()


def from_to_json(key):
    with open(get_json_filename(key), 'r', encoding='utf-16') as fp:
        data = json.load(fp)
        fp.close()
        return data


def for_each_key_do(action):
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    for key in alphabets:
        x = action(key)
        yield x


def fetch_data(key):
    print(f'searching for {key}')
    query(key)
    sleep(0.25)
    return 1


def transform(key):
    word_count = 0
    entries = []
    print(f'transforming for {key}')
    page = load(key)

    soup = BeautifulSoup(page, 'html.parser')

    results = soup.findAll("div", {"class": "hw_result"})

    if len(results) > 1:
        for i in range(0, len(results)):

            element = results[i]
            entry = {}
            for index, child in enumerate(element):
                if index == 0:
                    word = child.replace('\n', '').replace(')', '')
                    word = re.sub(r'\d+', '', word).strip()
                    entry['ks_word'] = transliterate_to_kashmiri(word)
                    entry['transliteration'] = word
                if index == 1:
                    sources = element.findChildren()[index]['src']
                    if len(sources) > 1:
                        entry['ks_pronunciation'] = sources
                if index == 4:
                    entry['en_meaning'] = child.replace('\n', '').replace(')', '').strip()
            entries.append(entry)
            word_count = word_count + 1

        export_to_json(key, entries)

    print(f'Total number of words for {key} = {word_count}')
    return word_count
