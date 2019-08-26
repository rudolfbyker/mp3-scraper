#!/usr/bin/env python3

from common import list_pages, sermon_pages, find_mp3, safe_title, extract_sermon_title
import csv


def main():
    domain = 'https://www.ligonier.org'
    path = '/learn/scripture/romans/'
    query = '?sort=scripture&type=sermon'
    idx = 0

    with open('download.list', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, [
            'download_url',
            'file_name',
        ])
        for list_soup in list_pages(domain, path, query):
            for sermon_soup in sermon_pages(list_soup, domain):
                mp3_url = domain + find_mp3(sermon_soup)
                print("Found {}".format(mp3_url))
                writer.writerow({
                    'download_url': mp3_url,
                    'file_name': "{:03d}_{}.mp3".format(
                        idx,
                        safe_title(extract_sermon_title(sermon_soup)),
                    ),
                })
                idx += 1


main()
