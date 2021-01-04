import argparse

from Extrator2 import fetch_data
from Extrator2 import for_each_key_do
from Extrator2 import transform

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Web scraper for DDSA")
    parser.add_argument("-d", "--download", action='store_true', help="downloading")
    parser.add_argument("-t", "--transform", action='store_true', help="transform")
    args = parser.parse_args()

    if args.download:
        print("Start scrapping from web")
        print(*for_each_key_do(lambda x: fetch_data(x)))
    if args.transform:
        print("Transforming to json ")
        total = sum(for_each_key_do(lambda x: transform(x)))
        print(f'Total number of words = {total}')
