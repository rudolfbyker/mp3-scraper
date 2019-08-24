#!/usr/bin/env python3

import csv
import wget
import os
from common import wait


def main():
    os.makedirs('downloads', exist_ok=True)
    with open('download.list', 'r') as csvfile:
        reader = csv.DictReader(csvfile, [
            'download_url',
            'file_name',
        ])
        for r in reader:
            url = r['download_url']
            path = os.path.join('downloads', r['file_name'])
            if os.path.exists(path):
                print("Already downloaded {} to {}".format(url, path))
            else:
                wait()
                print("Downloading {} to {}".format(url, path))
                wget.download(url, path)
                print()


main()
