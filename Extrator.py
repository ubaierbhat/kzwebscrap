import json
from time import sleep

import requests
from bs4 import BeautifulSoup

path_raw = './data/raw/'
path_json = './data/json/'
url = "http://www.kashmirizabaan.com/eng_ver.php"


def query(key):
    payload = f'meaning_target={key}&Submit=Go&lantype=hin&opt_dic=mat_like'
    headers = {
        'Connection': "keep-alive",
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept-Language': "en,et;q=0.9,ur;q=0.8",
    }
    page = requests.request("POST", url, data=payload, headers=headers)
    page.encoding = 'utf-8'

    # cleanup
    page_text = page.text
    page_text = page_text.replace("<table>", '')
    page_text = page_text.replace("&nbsp;", '')
    page_text = page_text.replace("</br>", '<br />')
    page_text = page_text.replace('<table width="717" border="0" bordercolor="#F0F0F0" bgcolor="#FFFFFF">', '<table>')
    page_text = page_text.replace('<font color="#CC6600">', '')
    page_text = page_text.replace('</div>\n\n</body>', '</body>')
    page_text = page_text.replace('<font face="Afan_Koshur_Naksh,Afan Koshur Naksh,Times New Roman" size=4>', '')
    page_text = page_text.replace('<font face=\\"Afan_Koshur_Naksh,Afan Koshur Naksh,Times New Roman\\" size=4>', '')
    page_text = page_text.replace(
        '<form name="dictionary" method="post" action=""onSubmit=return validate_form(this) >', '')
    page_text = page_text.replace('</div></th>', '<div></div></th>')

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
    alfabits = 'abcdefghijklmnopqrstuvwxyz'
    for ch1 in alfabits:
        for ch2 in alfabits:
            key = f'{ch1}{ch2}'
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

    tables = soup.find_all("table")

    if len(tables) > 1:
        for i in range(1, len(tables)):

            element = tables[i]

            tds = element.findAll('td')

            ks_word = tds[0].getText().strip()
            if ks_word == '' or ks_word == '۔۔۔':
                continue

            print('----------------------')

            category = tds[1].getText().strip()
            en_example = tds[2].getText().strip()
            hi_meaning = tds[3].getText().strip()
            ks_example = tds[4].getText().strip()
            en_meaning = tds[5].getText().strip()

            print(f'ks_word  = {ks_word}')
            print(f'category = {category}')
            print(f'en_example = {en_example}')
            print(f'hi_meaning = {hi_meaning}')
            print(f'ks_example = {ks_example}')
            print(f'en_meaning = {en_meaning}')

            entry = {
                'ks_word': ks_word,
                'category': category,
                'en_example': en_example,
                'ks_example': ks_example,
                'en_meaning': en_meaning
            }
            entries.append(entry)
            word_count = word_count + 1

        export_to_json(key, entries)

    print(f'Total number of words for {key} = {word_count}')
    return word_count
